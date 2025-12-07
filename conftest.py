import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Use environment variable or default to Docker internal network
BASE_URL = os.getenv('BASE_URL', 'http://frontend_ci:5173')

@pytest.fixture(scope="function")
def driver():
    """Create a Chrome WebDriver instance for testing"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Use system ChromeDriver (installed in Dockerfile)
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(15)
    
    yield driver
    driver.quit()

# Helper functions
def wait_for_element(driver, by, value, timeout=20):
    """Helper function to wait for element to be present"""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def wait_for_clickable(driver, by, value, timeout=20):
    """Helper function to wait for element to be clickable"""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
