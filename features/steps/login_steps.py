"""
Login steps implementation for Magento E-commerce - Core Requirements Only
"""
import time
from behave import step, then
from features.steps.pages.login_page import LoginPage as LP
from features.steps.pages.homepage import HomePage as HP


@step('I navigate to the Magento login page')
def step_given_navigate_to_login_page(context):
    """Navigate to the Magento login page"""
    context.current_page = LP(context.browser.driver)
    context.current_page.navigate_to_login_page()
    time.sleep(2)


@step('I login with valid credentials')
def step_when_login_with_valid_credentials(context):
    """Complete login process with valid credentials"""
    login_page: LP = context.current_page
    context.current_page = login_page.login_with_credentials()
    time.sleep(3)


@then('I should be redirected to the main page')
def step_then_redirected_to_main_page(context):
    """Verify redirection to main page after login"""
    # If not already on homepage, transition there
    if type(context.current_page).__name__ != 'HomePage':
        context.current_page = HP(context.browser.driver)
    
    home_page: HP = context.current_page
    assert home_page.verify_page_loaded(), "Main page did not load correctly"


@then('I should see the logout button or username confirming active session')
def step_then_see_logout_or_username(context):
    """Verify logout button or username is visible"""
    home_page: HP = context.current_page
    
    user_logged_in = home_page.verify_user_logged_in()
    logout_available = home_page.verify_logout_option_available()
    
    assert user_logged_in or logout_available, "Could not verify user is logged in" 