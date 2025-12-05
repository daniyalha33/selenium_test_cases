import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

BASE_URL = "http://34.239.165.164:8085"  # Updated URL

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    
    yield driver
    driver.quit()


def wait_for_element(driver, by, value, timeout=10):
    """Helper function to wait for element to be present"""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def wait_for_clickable(driver, by, value, timeout=10):
    """Helper function to wait for element to be clickable"""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


# SIGNUP TESTS
def test_signup_page_loads(driver):
    driver.get(BASE_URL)
    # Wait for the form to load - default state is Sign Up
    wait_for_element(driver, By.XPATH, "//p[contains(text(), 'Create Account')]")
    assert "Create Account" in driver.page_source


def test_valid_signup(driver):
    driver.get(BASE_URL)
    
    # Wait for form to load (default is signup)
    wait_for_element(driver, By.XPATH, "//input[@type='text']")
    
    # Fill in the signup form
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys("Test User")
    driver.find_element(By.XPATH, "//input[@type='date']").send_keys("01011990")
    driver.find_element(By.XPATH, "//select").send_keys("Male")
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("test@example.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Password123!")
    driver.find_element(By.XPATH, "//input[@type='number']").send_keys("1234567890")
    driver.find_element(By.XPATH, "//input[@placeholder='Address']").send_keys("123 Test St")
    
    # Click submit button
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Create Account')]")
    submit_button.click()
    
    time.sleep(2)


def test_signup_missing_fields(driver):
    driver.get(BASE_URL)
    
    # Wait for form
    wait_for_element(driver, By.XPATH, "//input[@type='email']")
    
    # Only fill email and password (missing required fields)
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("test@example.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Password123!")
    
    # Try to submit
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Create Account')]")
    submit_button.click()
    
    time.sleep(1)


def test_signup_invalid_email(driver):
    driver.get(BASE_URL)
    
    wait_for_element(driver, By.XPATH, "//input[@type='text']")
    
    # Fill form with invalid email
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys("Test User")
    driver.find_element(By.XPATH, "//input[@type='date']").send_keys("01011990")
    driver.find_element(By.XPATH, "//select").send_keys("Male")
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("invalidemail")  # Invalid email
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Password123!")
    driver.find_element(By.XPATH, "//input[@type='number']").send_keys("1234567890")
    driver.find_element(By.XPATH, "//input[@placeholder='Address']").send_keys("123 Test St")
    
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Create Account')]")
    submit_button.click()
    
    time.sleep(1)


def test_signup_weak_password(driver):
    driver.get(BASE_URL)
    
    wait_for_element(driver, By.XPATH, "//input[@type='text']")
    
    # Fill form with weak password
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys("Test User")
    driver.find_element(By.XPATH, "//input[@type='date']").send_keys("01011990")
    driver.find_element(By.XPATH, "//select").send_keys("Male")
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("test@example.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("123")  # Weak password
    driver.find_element(By.XPATH, "//input[@type='number']").send_keys("1234567890")
    driver.find_element(By.XPATH, "//input[@placeholder='Address']").send_keys("123 Test St")
    
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Create Account')]")
    submit_button.click()
    
    time.sleep(1)


def test_signup_missing_phone(driver):
    driver.get(BASE_URL)
    
    wait_for_element(driver, By.XPATH, "//input[@type='text']")
    
    # Fill everything except phone
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys("Test User")
    driver.find_element(By.XPATH, "//input[@type='date']").send_keys("01011990")
    driver.find_element(By.XPATH, "//select").send_keys("Male")
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("test@example.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Password123!")
    # Skip phone
    driver.find_element(By.XPATH, "//input[@placeholder='Address']").send_keys("123 Test St")
    
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Create Account')]")
    submit_button.click()
    
    time.sleep(1)


def test_signup_missing_address(driver):
    driver.get(BASE_URL)
    
    wait_for_element(driver, By.XPATH, "//input[@type='text']")
    
    # Fill everything except address
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys("Test User")
    driver.find_element(By.XPATH, "//input[@type='date']").send_keys("01011990")
    driver.find_element(By.XPATH, "//select").send_keys("Male")
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("test@example.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Password123!")
    driver.find_element(By.XPATH, "//input[@type='number']").send_keys("1234567890")
    # Skip address
    
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Create Account')]")
    submit_button.click()
    
    time.sleep(1)


# LOGIN TESTS
def test_login_page_loads(driver):
    driver.get(BASE_URL)
    
    # Wait for the page to load - it loads in signup mode by default
    wait_for_element(driver, By.XPATH, "//span[contains(text(), 'Login here')]")
    
    # Click to switch to login
    login_link = wait_for_clickable(driver, By.XPATH, "//span[contains(text(), 'Login here')]")
    login_link.click()
    
    # Wait and check for Login text
    time.sleep(1)
    wait_for_element(driver, By.XPATH, "//p[contains(text(), 'Login')]")
    assert "Login" in driver.page_source


def test_valid_login(driver):
    driver.get(BASE_URL)
    
    # Switch to login mode
    login_link = wait_for_clickable(driver, By.XPATH, "//span[contains(text(), 'Login here')]")
    login_link.click()
    
    time.sleep(1)
    
    # Fill login form
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("admin@test.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("password123")
    
    # Submit
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Login')]")
    submit_button.click()
    
    time.sleep(2)


def test_invalid_login(driver):
    driver.get(BASE_URL)
    
    # Switch to login mode
    login_link = wait_for_clickable(driver, By.XPATH, "//span[contains(text(), 'Login here')]")
    login_link.click()
    
    time.sleep(1)
    
    # Fill with wrong credentials
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("wrong@test.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("wrongpassword")
    
    # Submit
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Login')]")
    submit_button.click()
    
    time.sleep(2)
