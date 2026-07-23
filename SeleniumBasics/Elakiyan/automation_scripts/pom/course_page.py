from selenium.webdriver.common.by import By
from pom.base_page import BasePage

class CoursePage(BasePage):
    COURSE_NAME = (By.ID, "courseName")
    COURSE_CODE = (By.ID, "courseCode")
    SUBMIT_BTN = (By.ID, "submitCourse")
    SUCCESS_MSG = (By.ID, "successMessage")

    def create_course(self, name, code):
        self.type(self.COURSE_NAME, name)
        self.type(self.COURSE_CODE, code)
        self.click(self.SUBMIT_BTN)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)
