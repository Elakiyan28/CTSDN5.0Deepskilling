import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_simple_form_submission(driver):
    driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo")
    message_input = driver.find_element(By.ID, "user-message")
    message_input.send_keys("Hello Selenium")
    driver.find_element(By.ID, "showInput").click()
    output = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert output.text == "Hello Selenium"

def test_checkbox_demo(driver):
    driver.get("https://www.lambdatest.com/selenium-playground/checkbox-demo")
    checkbox = driver.find_element(By.ID, "isAgeSelected")
    checkbox.click()
    assert checkbox.is_selected()
    checkbox.click()
    assert not checkbox.is_selected()

@pytest.mark.parametrize("day", ["Monday", "Wednesday", "Friday"])
def test_dropdown_selection(driver, day):
    driver.get("https://www.lambdatest.com/selenium-playground/select-dropdown-demo")
    dropdown = driver.find_element(By.ID, "select-demo")
    dropdown.send_keys(day)
    selected = driver.find_element(By.CLASS_NAME, "selected-value")
    assert day in selected.text
