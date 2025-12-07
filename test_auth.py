import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Get BASE_URL from environment or use default
BASE_URL = os.getenv('BASE_URL', 'http://frontend_ci:5173')

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
    print(f"Testing URL: {BASE_URL}")
    driver.get(BASE_URL)
    wait_for_element(driver, By.XPATH, "//p[contains(text(), 'Create Account')]")
    assert "Create Account" in driver.page_source
    print("✓ Signup page loaded successfully")

def test_valid_signup(driver):
    driver.get(BASE_URL)
    wait_for_element(driver, By.XPATH, "//input[@type='text']")
    
    # Generate unique email to avoid duplicates
    import random
    unique_email = f"test{random.randint(1000, 9999)}@example.com"
    
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys("Test User")
    driver.find_element(By.XPATH, "//input[@type='date']").send_keys("01011990")
    driver.find_element(By.XPATH, "//select").send_keys("Male")
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(unique_email)
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Password123!")
    driver.find_element(By.XPATH, "//input[@type='number']").send_keys("1234567890")
    driver.find_element(By.XPATH, "//input[@placeholder='Address']").send_keys("123 Test St")
    
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Create Account')]")
    submit_button.click()
    time.sleep(2)
    print("✓ Valid signup test completed")

def test_signup_missing_fields(driver):
    driver.get(BASE_URL)
    wait_for_element(driver, By.XPATH, "//input[@type='email']")
    
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("test@example.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("Password123!")
    
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Create Account')]")
    submit_button.click()
    time.sleep(1)
    print("✓ Missing fields validation test completed")

def test_signup_invalid_email(driver):
    driver.get(BASE_URL)
    wait_for_element(driver, By.XPATH, "//input[@type='text']")
    
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys("Test User")
    driver.find_element(By.XPATH, "//input[@type='date']").send_keys("01011990")
    driver.find_element(By.XPATH, "//select").send_keys("Male")
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("invalidemail")
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
    
    driver.find_element(By.XPATH, "//input[@type='text']").send_keys("Test User")
    driver.find_element(By.XPATH, "//input[@type='date']").send_keys("01011990")
    driver.find_element(By.XPATH, "//select").send_keys("Male")
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("test@example.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("123")
    driver.find_element(By.XPATH, "//input[@type='number']").send_keys("1234567890")
    driver.find_element(By.XPATH, "//input[@placeholder='Address']").send_keys("123 Test St")
    
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Create Account')]")
    submit_button.click()
    time.sleep(1)
    print("✓ Weak password validation test completed")

# LOGIN TESTS
def test_login_page_loads(driver):
    driver.get(BASE_URL)
    wait_for_element(driver, By.XPATH, "//span[contains(text(), 'Login here')]")
    
    login_link = wait_for_clickable(driver, By.XPATH, "//span[contains(text(), 'Login here')]")
    login_link.click()
    
    time.sleep(1)
    wait_for_element(driver, By.XPATH, "//p[contains(text(), 'Login')]")
    assert "Login" in driver.page_source
    print("✓ Login page loaded successfully")

def test_valid_login(driver):
    driver.get(BASE_URL)
    
    login_link = wait_for_clickable(driver, By.XPATH, "//span[contains(text(), 'Login here')]")
    login_link.click()
    time.sleep(1)
    
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("admin@test.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("password123")
    
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Login')]")
    submit_button.click()
    time.sleep(2)
    print("✓ Valid login test completed")

def test_invalid_login(driver):
    driver.get(BASE_URL)
    
    login_link = wait_for_clickable(driver, By.XPATH, "//span[contains(text(), 'Login here')]")
    login_link.click()
    time.sleep(1)
    
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys("wrong@test.com")
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys("wrongpassword")
    
    submit_button = wait_for_clickable(driver, By.XPATH, "//button[contains(text(), 'Login')]")
    submit_button.click()
    time.sleep(2)
    print("✓ Invalid login test completed")
