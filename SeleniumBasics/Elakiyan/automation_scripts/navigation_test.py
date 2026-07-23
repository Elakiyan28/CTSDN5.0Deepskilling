from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open Playground
    driver.get("https://www.lambdatest.com/selenium-playground/")

    # Navigate to Simple Form Demo
    simple_form_link = driver.find_element("link text", "Simple Form Demo")
    simple_form_link.click()

    # Assert URL contains 'simple-form-demo'
    assert "simple-form-demo" in driver.current_url
    print("Navigated to Simple Form Demo successfully.")

    # Navigate back
    driver.back()

    # Open new tab (Google)
    driver.execute_script("window.open('https://www.google.com');")
    tabs = driver.window_handles

    # Switch to new tab
    driver.switch_to.window(tabs[1])
    print("Google Tab Title:", driver.title)

    # Switch back to Playground tab
    driver.switch_to.window(tabs[0])

    # Take screenshot
    driver.save_screenshot("playground_screenshot.png")
    print("Screenshot saved as playground_screenshot.png")

    # Window size
    print("Current size:", driver.get_window_size())
    driver.set_window_size(1280, 800)
    print("Resized window to 1280x800")

    driver.quit()

if __name__ == "__main__":
    main()
