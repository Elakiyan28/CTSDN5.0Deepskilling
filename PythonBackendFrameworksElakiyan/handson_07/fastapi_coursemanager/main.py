from contextlib import asynccontextmanager
from datetime import date
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from models import Course, Student, Enrollment
from schemas import (
    CourseCreate, CourseUpdate, CourseResponse,
    StudentCreate, StudentResponse,
    EnrollmentCreate, EnrollmentResponse,
)


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


@app.get('/', tags=['Root'])
async def root():
    return {'message': 'API running'}


# ---------- Courses ----------

@app.post(
    '/api/courses/',
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
    return new_course


@app.get('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@app.get('/api/courses/', response_model=list[CourseResponse], tags=['Courses'])
async def list_courses(
    skip: int = 0,
    limit: int = 10,
    department_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Course)
    if department_id is not None:
        query = query.where(Course.department_id == department_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@app.put('/api/courses/{course_id}', response_model=CourseResponse, tags=['Courses'])
async def update_course(course_id: int, payload: CourseUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    await db.delete(course)
    await db.commit()


@app.get('/api/courses/{course_id}/students/', response_model=list[StudentResponse], tags=['Courses'])
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db)):
    query = (
        select(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .where(Enrollment.course_id == course_id)
    )
    result = await db.execute(query)
    return result.scalars().all()


# ---------- Students ----------

@app.post('/api/students/', response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=['Students'])
async def create_student(student: StudentCreate, db: AsyncSession = Depends(get_db)):
    new_student = Student(**student.model_dump())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


@app.get('/api/students/', response_model=list[StudentResponse], tags=['Students'])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()


@app.get('/api/students/{student_id}', response_model=StudentResponse, tags=['Students'])
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    return student


@app.put('/api/students/{student_id}', response_model=StudentResponse, tags=['Students'])
async def update_student(student_id: int, payload: StudentCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    for field, value in payload.model_dump().items():
        setattr(student, field, value)
    await db.commit()
    await db.refresh(student)
    return student


@app.delete('/api/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Students'])
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail='Student not found')
    await db.delete(student)
    await db.commit()


# ---------- Enrollments ----------

@app.post('/api/enrollments/', response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED, tags=['Enrollments'])
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


@app.get('/api/enrollments/', response_model=list[EnrollmentResponse], tags=['Enrollments'])
async def list_enrollments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Enrollment))
    return result.scalars().all()
