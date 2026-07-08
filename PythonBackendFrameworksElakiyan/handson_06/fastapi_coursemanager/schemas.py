from typing import Optional, List
from pydantic import BaseModel


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
