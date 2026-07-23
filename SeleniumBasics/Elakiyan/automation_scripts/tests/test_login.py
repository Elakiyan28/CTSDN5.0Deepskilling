import pytest
from pom.login_page import LoginPage

def test_valid_login(driver, base_url):
    login_page = LoginPage(driver)
    login_page.open(f"{base_url}/login")
    login_page.login("admin", "password123")
    assert "Dashboard" in driver.title
