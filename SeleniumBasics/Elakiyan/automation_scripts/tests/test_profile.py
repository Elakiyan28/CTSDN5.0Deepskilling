import pytest
from pom.profile_page import ProfilePage

def test_profile_details(driver, base_url):
    profile_page = ProfilePage(driver)
    profile_page.open(f"{base_url}/profile")
    assert profile_page.get_name() == "Elakiyan"
    assert "@" in profile_page.get_email()
