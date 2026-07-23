from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.lambdatest.com/selenium-playground/")

# Navigate to Simple Form Demo
driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

# Locate input field using different strategies
driver.find_element(By.ID, "user-message").send_keys("Hello by ID")
driver.find_element(By.NAME, "message").clear()
driver.find_element(By.NAME, "message").send_keys("Hello by NAME")

# CSS Selector examples
driver.find_element(By.CSS_SELECTOR, "#user-message").clear()
driver.find_element(By.CSS_SELECTOR, "[name='message']").send_keys("Hello by CSS")

# XPath examples
driver.find_element(By.XPATH, "//input[@id='user-message']").clear()
driver.find_element(By.XPATH, "//input[@id='user-message']").send_keys("Hello by XPath")

# Explicit Wait for alert
driver.get("https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo")
driver.find_element(By.ID, "button-success").click()
alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
)
assert "successfully" in alert.text

driver.quit()
