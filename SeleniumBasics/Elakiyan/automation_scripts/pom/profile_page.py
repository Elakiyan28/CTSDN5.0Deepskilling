from selenium.webdriver.common.by import By
from pom.base_page import BasePage

class ProfilePage(BasePage):
    NAME_FIELD = (By.ID, "profileName")
    EMAIL_FIELD = (By.ID, "profileEmail")

    def get_name(self):
        return self.get_text(self.NAME_FIELD)

    def get_email(self):
        return self.get_text(self.EMAIL_FIELD)
