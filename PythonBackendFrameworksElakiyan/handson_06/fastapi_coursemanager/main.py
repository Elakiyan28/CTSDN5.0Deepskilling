from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from models import Course
from schemas import CourseCreate, CourseResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title='Course Management API', version='1.0', lifespan=lifespan)


@app.get('/')
async def root():
    return {'message': 'API running'}


@app.post('/api/courses/', response_model=CourseResponse)
async def create_course(course: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.get('/api/courses/{course_id}', response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@app.get('/api/courses/', response_model=list[CourseResponse])
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
