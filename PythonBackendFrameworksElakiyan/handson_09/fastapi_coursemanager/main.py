from contextlib import asynccontextmanager
from datetime import date
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from models import Course, Student, Enrollment, User
from security import get_password_hash, verify_password, create_access_token, decode_access_token
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse,
    UserCreate, UserResponse, Token,
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


# --- Step 94: CORS ---
# CORS is enforced by the browser, not the server - it tells the browser
# which origins may call this API from JS. Server-to-server calls (curl,
# Postman, another backend) are never blocked by CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{V1}/auth/login/')


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


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = decode_access_token(token)
        email = payload.get('sub')
        if email is None:
            raise HTTPException(status_code=401, detail='Invalid token')
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid or expired token')

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    return user


# ---------- Auth ----------

@app.post(f'{V1}/auth/register/', response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=['Auth'])
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail='Email already registered')

    # Never store or log the plain-text password - only the bcrypt hash.
    user = User(email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@app.post(f'{V1}/auth/login/', response_model=Token, tags=['Auth'])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Incorrect email or password')

    access_token = create_access_token({'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


# --- Step 95: OAuth2 Authorization Code flow vs this simple JWT login ---
# Authorization Code flow: user is redirected to a separate auth server,
# logs in there, the auth server redirects back with a short-lived `code`,
# which the client exchanges (server-to-server, with a client secret) for
# an access token. The user's password is never seen by our app at all -
# used for "Login with Google" style flows.
# Our flow here: the client sends email+password directly to OUR server,
# which verifies it and hands back a JWT itself. Simpler, but only works
# because client and API are the same trust boundary - the client must be
# trusted with the raw password.


# ---------- Courses ----------

@app.post(
    f'{V1}/courses/',
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    summary='Create a new course',
    response_description='The created course',
)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
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
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
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
