import pytest
from pom.course_page import CoursePage

def test_create_course(driver, base_url):
    course_page = CoursePage(driver)
    course_page.open(f"{base_url}/courses")
    course_page.create_course("Data Structures", "CS101")
    assert "Course created successfully" in course_page.get_success_message()
