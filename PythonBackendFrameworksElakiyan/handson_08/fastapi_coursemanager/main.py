from contextlib import asynccontextmanager
from datetime import date
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from models import Course, Student, Enrollment
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse,
)

# --- Step 78-79: Naming/method audit ---
# All resources below are already plural nouns (courses/students/enrollments),
# GET has no side effects, POST creates, PUT replaces, PATCH partially updates,
# DELETE removes. No verbs in URLs (no /getCourses/ etc).

# --- Step 82: API Versioning ---
# Chose URL versioning (/api/v1/...) over header versioning
# (Accept: application/vnd.api+json;version=1) because URL versioning is
# visible, cacheable, and trivially testable in a browser/curl. Header
# versioning keeps URLs clean across versions but is harder to discover
# and test, and proxies/CDNs cache by URL so it can complicate caching.
V1 = '/api/v1'


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title='Course Management API',
    description='Backend API for managing departments, courses, students, and enrollments.',
    version='1.0',
    contact={'name': 'Femilin', 'email': 'femilin@college.edu'},
    lifespan=lifespan,
)


def send_confirmation_email(student_email: str):
    print(f'Sending confirmation to {student_email}')


# --- Step 85: Standardised error envelope ---
# {'error': {'code': 'NOT_FOUND', 'message': '...', 'field': None}}
ERROR_CODES = {
    400: 'BAD_REQUEST',
    401: 'UNAUTHORIZED',
    404: 'NOT_FOUND',
    409: 'CONFLICT',
    422: 'UNPROCESSABLE_ENTITY',
}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    code = ERROR_CODES.get(exc.status_code, 'ERROR')
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': {'code': code, 'message': exc.detail, 'field': None}},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0] if exc.errors() else {}
    field = first.get('loc', [None])[-1]
    return JSONResponse(
        status_code=422,
        content={'error': {'code': 'VALIDATION_ERROR', 'message': first.get('msg', 'Validation failed'), 'field': field}},
    )


@app.get('/', tags=['Root'])
async def root():
    return {'message': 'API running'}


# ---------- Courses ----------

@app.post(
    f'{V1}/courses/',
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    summary='Create a new course',
    response_description='The created course',
)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    # Step 81: Location header pointing to the new resource
    headers = {'Location': f'{V1}/courses/{new_course.id}/'}
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CourseResponse.model_validate(new_course).model_dump(),
        headers=headers,
    )


@app.get(f'{V1}/courses/{{course_id}}/', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    return course


@app.get(f'{V1}/courses/', tags=['Courses'])
async def list_courses(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    # Step 83-84: offset pagination envelope + case-insensitive search
    query = select(Course)
    count_query = select(func.count()).select_from(Course)

    if search:
        like = f'%{search}%'
        condition = or_(Course.name.ilike(like), Course.code.ilike(like))
        query = query.where(condition)
        count_query = count_query.where(condition)

    total = (await db.execute(count_query)).scalar_one()
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    courses = (await db.execute(query)).scalars().all()

    has_next = offset + page_size < total
    has_prev = page > 1
    next_url = f'{V1}/courses/?page={page + 1}&page_size={page_size}' if has_next else None
    prev_url = f'{V1}/courses/?page={page - 1}&page_size={page_size}' if has_prev else None

    return {
        'count': total,
        'next': next_url,
        'previous': prev_url,
        'results': [CourseResponse.model_validate(c).model_dump() for c in courses],
    }


@app.put(f'{V1}/courses/{{course_id}}/', response_model=CourseResponse, tags=['Courses'])
async def update_course(course_id: int, payload: CourseUpdate, db: AsyncSession = Depends(get_db)):
    course = await _get_course_or_404(course_id, db)
    for field, value in payload.model_dump().items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


# Step 79: PATCH alongside PUT - partial update, only supplied fields change
@app.patch(f'{V1}/courses/{{course_id}}/', response_model=CourseResponse, tags=['Courses'])
async def partial_update_course(course_id: int, payload: CourseUpdate, db: AsyncSession = Depends(get_db)):
    course = await _get_course_or_404(course_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.delete(f'{V1}/courses/{{course_id}}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await _get_course_or_404(course_id, db)
    await db.delete(course)
    await db.commit()


@app.get(f'{V1}/courses/{{course_id}}/students/', response_model=list[StudentResponse], tags=['Courses'])
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    query = (
        select(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .where(Enrollment.course_id == course_id)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def _get_course_or_404(course_id: int, db: AsyncSession) -> Course:
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail=f'Course with id {course_id} does not exist')
    return course


# ---------- Students ----------

@app.post(f'{V1}/students/', response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=['Students'])
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    new_student = Student(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


@app.get(f'{V1}/students/', response_model=list[StudentResponse], tags=['Students'])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.get(f'{V1}/students/{{student_id}}/', response_model=StudentResponse, tags=['Students'])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail=f'Student with id {student_id} does not exist')
    return student


# ---------- Enrollments ----------

@app.post(f'{V1}/enrollments/', response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED, tags=['Enrollments'])
async def create_enrollment(
    enrollment: EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    new_enrollment = Enrollment(**enrollment.model_dump(), enrollment_date=date.today())
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    result = await db.execute(select(Student).where(Student.id == new_enrollment.student_id))
    student = result.scalar_one_or_none()
    if student:
        background_tasks.add_task(send_confirmation_email, student.email)

    return new_enrollment


@app.get(f'{V1}/enrollments/', response_model=list[EnrollmentResponse], tags=['Enrollments'])
async def list_enrollments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Enrollment))
    return result.scalars().all()
