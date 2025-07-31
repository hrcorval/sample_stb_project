"""
Login Page Object Model for Magento E-commerce
"""
import logging
from selenium.webdriver.common.by import By
from features.steps.pages.base_page import BasePage

class LoginPage(BasePage):
    """Login page object model for Magento"""
    
    # Page locators for Magento login page
    email_field = (By.ID, "email")
    password_field = (By.ID, "pass")
    login_button = (By.ID, "send2")
    error_message = (By.XPATH, "//div[contains(@class,'message-error')]")
    forgot_password_link = (By.XPATH, "//a[contains(@class,'action remind')]")
    create_account_link = (By.XPATH, "//a[contains(@class,'action create')]")
    
    # Post-login verification elements
    welcome_message = (By.XPATH, "//span[contains(@class,'logged-in')]")
    account_menu = (By.XPATH, "//button[@data-action='customer-menu-toggle']")
    logout_link = (By.XPATH, "//a[contains(@href,'customer/account/logout')]")
    my_account_link = (By.XPATH, "//a[contains(@href,'customer/account')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_login_page(self):
        """Navigate to the Magento login page"""
        login_url = self.config.get('magento_website', 'login_url')
        self.web_utils.get(login_url, wait_for_page_load=True)
    
    def enter_email(self, email):
        """Enter email address"""
        email_element = self.web_utils.find_element(*self.email_field)
        email_element.clear()
        email_element.send_keys(email)
    
    def enter_password(self, password):
        """Enter password"""
        password_element = self.web_utils.find_element(*self.password_field)
        password_element.clear()
        password_element.send_keys(password)
    
    def click_login_button(self):
        """Click login button"""
        login_btn = self.web_utils.find_element(*self.login_button)
        self.web_utils.safe_click(login_btn)
    
    def get_error_message(self):
        """Get error message text"""
        try:
            error_element = self.web_utils.find_element(*self.error_message, retries=3)
            return error_element.text
        except Exception as e:
            logging.info("No error message found on login page")
            return ""
    
    def login_with_credentials(self, email=None, password=None):
        """Complete login process with provided or default credentials - returns HomePage"""
        if not email:
            email = self.config.get('test_credentials', 'email')
        if not password:
            password = self.config.get('test_credentials', 'password')
            
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        
        # Import here to avoid circular imports
        from features.steps.pages.homepage import HomePage
        return HomePage(self.driver)
    
    def is_logged_in(self):
        """Verify if user is successfully logged in"""
        try:
            # Check for account menu or welcome message
            self.web_utils.find_element(*self.account_menu, retries=5)
            return True
        except:
            # Alternative check for welcome message or my account link
            try:
                self.web_utils.find_element(*self.my_account_link, retries=3)
                return True
            except:
                return False
    
    def verify_login_success(self):
        """Verify successful login and return to appropriate page"""
        if self.is_logged_in():
            return True
        else:
            error_msg = self.get_error_message()
            raise AssertionError(f"Login failed. Error: {error_msg}") 