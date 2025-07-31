import time
import logging
import configparser
import os
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as exp_cond
from selenium.common.exceptions import TimeoutException
from features.steps.pages.web_utils import WebUtils

class BasePage:

    xpath_lower_text = "translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"
    ad_blocker_dismiss_button = (By.ID, "dismiss-button")
    
    # Category navigation locator
    category_menu_item = (By.XPATH, "//li[contains(@class, 'level{}') and @role='presentation']//a/span[" + xpath_lower_text + "='{}']")
    category_submenu_item = (By.XPATH, "//ul[@aria-expanded='true']//li[contains(@class, 'level{}') and @role='presentation']//a/span[" + xpath_lower_text + "='{}']")
    
    # Common cart locators
    cart_icon = (By.XPATH, "//div[contains(@class, 'minicart-wrapper')]//a[contains(@class,'showcart')]")
    cart_counter = (By.XPATH, "//div[contains(@class, 'minicart-wrapper')]//span[@class='counter-number']")
    view_cart_link = (By.XPATH, "//div[@id='minicart-content-wrapper']//a[contains(@href,'checkout/cart') and contains(@class,'viewcart')]//span")
    
    # Common navigation menu locators
    women_menu = (By.XPATH, "//a[@id='ui-id-4']//span[text()='Women']")
    men_menu = (By.XPATH, "//a[@id='ui-id-5']//span[text()='Men']")
    gear_menu = (By.XPATH, "//a[@id='ui-id-6']//span[text()='Gear']")
    training_menu = (By.XPATH, "//a[@id='ui-id-7']//span[text()='Training']")
    sale_menu = (By.XPATH, "//a[@id='ui-id-8']//span[text()='Sale']")

    def __init__(self, driver):
        self.driver = driver
        self.web_utils = WebUtils(driver)
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from config file"""
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), "../../../config/config.cfg")
        config.read(config_path)
        return config

    def get_cart_counter(self):
        """Get current cart item count"""
        try:
            counter_element = self.web_utils.find_element(*self.cart_counter, retries=3)
            return int(counter_element.text)
        except Exception as e:
            logging.warning("Cart counter element not found")
            return 0

    def open_cart(self):
        """Open the shopping cart"""
        try:
            cart_icon_element = self.web_utils.find_element(*self.cart_icon)
            self.web_utils.safe_click(cart_icon_element)
        except Exception as e:
            logging.warning("Cart icon not found or not clickable")

    def open_cart_page(self):
        """Navigate to cart page and return CartPage"""
        # Use inherited open_cart method first
        self.open_cart()
        time.sleep(1)
        
        # Click on view cart link from mini cart
        try:
            view_cart_element = self.web_utils.find_element(*self.view_cart_link)
            self.web_utils.safe_click(view_cart_element)
            
            # Import here to avoid circular imports
            from features.steps.pages.cart_page import CartPage
            return CartPage(self.driver)
        except Exception as e:
            logging.warning("View cart link not found or not clickable")
            return None

    def open_product_page(self):
        """Navigate to product page and return ProductPage"""
        women_element = self.web_utils.find_element(*self.women_menu)
        self.web_utils.safe_click(women_element)
        
        # Import here to avoid circular imports
        from features.steps.pages.product_page import ProductPage
        return ProductPage(self.driver)

    def get_current_url(self):
        return self.driver.current_url

    def go_to_previous_page(self):
        return self.driver.back()

    def refresh_page(self, seconds):
        self.driver.refresh()
        time.sleep(int(seconds))

    def go_back(self):
        self.driver.back() 


    def select_product_categories_from_top_menu(self, categories_list):
        """Select categories from top navigation menu"""
        for i in range(len(categories_list)):
            category_level = i
            category_name = categories_list[i]
            if category_level == 0:
                category_element = self.web_utils.find_element(self.category_menu_item[0], 
                                                               self.category_menu_item[1].format(str(category_level), 
                                                                                                 category_name.lower()))
            else:
                category_element = self.web_utils.find_element(self.category_submenu_item[0], 
                                                               self.category_submenu_item[1].format(str(category_level), 
                                                                                                    category_name.lower()))
            self.web_utils.mouse_hover(category_element)
            time.sleep(0.5)
            if i + 1 == len(categories_list):
                self.web_utils.safe_click(category_element)
                time.sleep(1)
        from features.steps.pages.product_page import ProductPage
        return ProductPage(self.driver)