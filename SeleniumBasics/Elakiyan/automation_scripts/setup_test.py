"""
Hands-On 4: Selenium WebDriver Setup
Components:
- WebDriver: Controls browser via driver.
- Selenium Grid: Runs tests in parallel across machines/browsers.
- Selenium IDE: Record/playback tool for quick automation.
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main():
    # Chrome options
    options = Options()
    # Run in headless mode (no visible browser window)
    options.add_argument("--headless")

    # Setup driver with webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Implicit wait (not recommended globally, explicit waits are better)
    driver.implicitly_wait(10)

    # Navigate to Selenium Playground
    driver.get("https://www.lambdatest.com/selenium-playground/")
    print("Page Title:", driver.title)

    # Close browser
    driver.quit()

if __name__ == "__main__":
    main()
