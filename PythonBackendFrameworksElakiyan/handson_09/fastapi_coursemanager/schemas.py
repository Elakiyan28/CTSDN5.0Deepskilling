from typing import Optional, List
from datetime import date
from pydantic import BaseModel, EmailStr


class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    model_config = {'from_attributes': True}


class DepartmentResponse(BaseModel):
    id: int
    name: str
    head_of_dept: Optional[str] = None
    budget: Optional[float] = None
    courses: List[CourseResponse] = []

    model_config = {'from_attributes': True}


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    department_id: int
    enrollment_year: int


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department_id: int
    enrollment_year: int

    model_config = {'from_attributes': True}


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: Optional[date] = None
    grade: Optional[str] = None

    model_config = {'from_attributes': True}


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

    model_config = {'from_attributes': True}


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
