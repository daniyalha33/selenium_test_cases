import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Get BASE_URL from environment variable (for Docker) or use localhost (for local testing)
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5173')

# Append /login if your app loads on /login route
if not BASE_URL.endswith('/login'):
    BASE_URL = f"{BASE_URL}/login"

print(f"[INFO] Using BASE_URL: {BASE_URL}")

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


# SIGNUP TESTS
def test_signup_page_loads(driver):
    print(f"Testing URL: {BASE_URL}")
    driver.get(BASE_URL)
    
    # Wait a bit for page to render
    time.sleep(2)
    
    # Wait for the form to load - default state is Sign Up
    try:
        wait_for_element(driver, By.XPATH, "//p[contains(text(), 'Create Account')]")
        assert "Create Account" in driver.page_source
        print("✓ Signup page loaded successfully")
    except Exception as e:
        print(f"❌ Error loading signup page: {e}")
        print(f"Page Title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        print(f"Page Source (first 1000 chars):\n{driver.page_source[:1000]}")
        raise


def test_valid_signup(driver):
    driver.get(BASE_URL)
    
    # Wait for form to load (default is signup)
    wait_for_element(driver, By.XPATH, "//input[@type='text']")
    
    # Generate unique email to avoid duplicates
    import random
    unique_email = f"test{random.randint(1000, 9999)}@example.com"
    
    # Fill in the signup form
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys("Test User")
    driver.find_element(By.XPATH, "//input[@type='date']").send_keys("01011990")
    driver.find_element(By.XPATH, "//select").send_keys("Male")
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(unique_email)
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Password123!")
    driver.find_element(By.XPATH, "//input[@type='number']").send_keys("1234567890")
    driver.find_element(By.XPATH, "//input[@placeholder='Address']").send_keys("123 Test St")
    
    # Click submit button
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Create Account')]")
    submit_button.click()
    
    time.sleep(2)
    print("✓ Valid signup test completed")


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
    print("✓ Missing fields validation test completed")


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
    print("✓ Invalid email validation test completed")


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
    print("✓ Weak password validation test completed")


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
    print("✓ Missing phone validation test completed")


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
    print("✓ Missing address validation test completed")


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
    print("✓ Login page loaded successfully")


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
    print("✓ Valid login test completed")


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
    print("✓ Invalid login test completed")
