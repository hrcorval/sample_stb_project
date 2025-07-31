"""
Homepage/Dashboard Page Object Model for Magento E-commerce
"""
import logging
from selenium.webdriver.common.by import By
from features.steps.pages.base_page import BasePage


class HomePage(BasePage):
    """Homepage/Dashboard page object model"""
    
    # Header navigation locators
    logo = (By.XPATH, "//a[@class='logo']")
    search_box = (By.ID, "search")
    search_button = (By.XPATH, "//button[@title='Search']")
    
    # User account locators
    account_menu = (By.XPATH, "//button[@data-action='customer-menu-toggle']")
    welcome_message = (By.XPATH, "//span[contains(@class,'logged-in')]")
    my_account_link = (By.XPATH, "//a[contains(@href,'customer/account')]")
    my_orders_link = (By.XPATH, "//a[contains(@href,'sales/order/history')]")
    logout_link = (By.XPATH, "//a[contains(@href,'customer/account/logout')]")
    
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_homepage(self):
        """Navigate to the Magento homepage"""
        base_url = self.config.get('magento_website', 'base_url')
        self.web_utils.get(base_url, wait_for_page_load=True)
    
    def verify_page_loaded(self):
        """Verify that the homepage has loaded correctly"""
        try:
            self.web_utils.find_element(*self.logo, retries=5)
            return True
        except Exception as e:
            logging.warning("Homepage logo not found - page may not have loaded correctly")
            return False
    
    def verify_user_logged_in(self):
        """Verify that user is logged in by checking for account menu or welcome message"""
        try:
            self.web_utils.find_element(*self.account_menu, retries=5)
            return True
        except:
            try:
                self.web_utils.find_element(*self.welcome_message, retries=3)
                return True
            except:
                return False
    
    def open_account_menu(self):
        """Open the user account dropdown menu"""
        account_menu_element = self.web_utils.find_element(*self.account_menu)
        self.web_utils.safe_click(account_menu_element)
    
    def verify_logout_option_available(self):
        """Verify that logout option is available in account menu"""
        try:
            self.open_account_menu()
            self.web_utils.find_element(*self.logout_link, retries=3)
            return True
        except:
            return False 