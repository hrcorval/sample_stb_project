"""
Product Page Object Model for Magento E-commerce
"""
import logging
import time
from selenium.webdriver.common.by import By
from features.steps.pages.base_page import BasePage
from features.steps.pages.web_utils import wait_and_close_adds_popups

class ProductPage(BasePage):
    """Product listing and product details page object model"""
    
    # Category page locators
    tops_category = (By.XPATH, "//a[contains(@href,'women/tops-women')]")
    
    # Product listing page locators
    product_items = (By.XPATH, "//div[@class='product-item-info']")
    product_names = (By.XPATH, "//a[@class='product-item-link']")
    add_to_cart_button = (By.ID, "product-addtocart-button")
    
    # Success messages
    success_message = (By.XPATH, "//div[contains(@data-ui-id,'message-success')]")
    
    # Product options
    size_options = (By.XPATH, "//div[@class='swatch-option text']")
    size_option = (By.XPATH, "//div[@class='swatch-option text' and @option-label='{}']")
    color_options = (By.XPATH, "//div[@class='swatch-option color']")
    color_option = (By.XPATH, "//div[@class='swatch-option color' and @option-label='{}']")

    product_name = (By.XPATH, "//div[contains(@class, 'page-title-wrapper')]//span[@itemprop='name']")
    product_price = (By.XPATH, "//div[@class='product-info-price']//span[@data-price-amount]")
    quantity_input = (By.XPATH, "//div[@class='product-add-form']//input[@id='qty']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to_tops_category(self):
        """Navigate to women's tops category"""
        women_element = self.web_utils.find_element(*self.women_menu)
        self.web_utils.safe_click(women_element)
        time.sleep(1)
        tops_element = self.web_utils.find_element(*self.tops_category)
        self.web_utils.safe_click(tops_element)
    
    def click_product_by_index(self, index=0):
        """Click on a product by index (0-based)"""
        products = self.web_utils.find_elements(*self.product_names)
        if index < len(products):
            retries = 2
            for _ in range(retries):
                product_name = products[index].text
                self.web_utils.safe_click(products[index])
                time.sleep(1)
                if wait_and_close_adds_popups(self.driver):
                    time.sleep(1)
                else:
                    break
            return product_name
        else:
            raise IndexError(f"Product index {index} not found")
    
    def select_product_size(self, size=None):
        """Select product size"""
        if not size or size.lower() == 'any':
            size_element = self.web_utils.find_element(*self.size_options)
        else:
            size_element = self.web_utils.find_element(self.size_option[0], self.size_option[1].format(size))
        self.web_utils.safe_click(size_element)
        time.sleep(1)

    def select_product_color(self, color=None):
        """Select product color"""
        if not color or color.lower() == 'any':
            color_element = self.web_utils.find_element(*self.color_options)
        else:
            color_element = self.web_utils.find_element(self.color_option[0], self.color_option[1].format(color))
        self.web_utils.safe_click(color_element)
        time.sleep(1)

    def select_product_quantity(self, quantity=1):
        """Select product quantity"""
        pass

    def add_product_to_cart(self):
        """Add current product to cart"""
        product_data = {}
        product_data['name'] = self.web_utils.find_element(*self.product_name, wait_for_clickable=False).text
        product_data['price'] = self.web_utils.find_element(*self.product_price, wait_for_clickable=False).text
        product_data['quantity'] = int(self.web_utils.find_element(*self.quantity_input).get_attribute('value'))
        add_to_cart_btn = self.web_utils.find_element(*self.add_to_cart_button)
        self.web_utils.safe_click(add_to_cart_btn)        
        return product_data
    
    def verify_add_to_cart_success(self):
        """Verify that product was successfully added to cart"""
        try:
            self.web_utils.find_element(*self.success_message, retries=5)
            return True
        except Exception as e:
            logging.warning("Add to cart success message not found")
            return False
    
    # get_cart_counter and open_cart_page methods now inherited from BasePage
    
    def go_back_to_product_listing(self):
        """Go back to product listing - returns ProductPage (same type)"""
        self.navigate_to_tops_category()
        return ProductPage(self.driver)
