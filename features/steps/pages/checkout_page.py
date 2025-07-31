"""
Checkout Page Object Model for Magento E-commerce
"""
import logging
import time
from selenium.webdriver.common.by import By
from features.steps.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Checkout page object model"""
    
    # Shipping information form locators
    email_field = (By.ID, "customer-email")
    first_name_field = (By.NAME, "firstname")
    last_name_field = (By.NAME, "lastname")
    street_address_field = (By.NAME, "street[0]")
    city_field = (By.NAME, "city")
    state_field = (By.NAME, "region_id")
    state_dropdown = (By.XPATH, ".//select[@name='region_id']//option[@data-title]")
    postal_code_field = (By.NAME, "postcode")
    phone_field = (By.NAME, "telephone")
    
    # Shipping method locators
    shipping_methods = (By.XPATH, "//div[@id='checkout-shipping-method-load']//input[contains(@name, 'ko_unique_')]")
    
    # Navigation buttons
    next_button = (By.XPATH, "//button[@data-role='opc-continue']")
    
    # Payment method locators
    payment_methods = (By.XPATH, "//input[@name='payment[method]']")
    
    # Order review locators
    place_order_button = (By.XPATH, "//button[@title='Place Order']")
    
    # Order confirmation locators
    success_message = (By.XPATH, "//span[contains(text(),'Thank you for your purchase!')]")
    order_confirmation_message = (By.XPATH, "//p[contains(text(),'Your order number is')]")

    address_items = (By.XPATH, "//div[contains(@class, 'shipping-address-item')]")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_address_already_filled(self):
        """Check if address is already filled"""
        try:
            self.web_utils.find_element(*self.address_items, retries=1)
            return True
        except:
            return False

    def fill_shipping_information(self):
        """Fill out shipping information form with config data"""
        # Fill first name
        first_name_element = self.web_utils.find_element(*self.first_name_field)
        first_name_element.clear()
        first_name_element.send_keys(self.config.get('checkout_data', 'first_name'))
        
        # Fill last name
        last_name_element = self.web_utils.find_element(*self.last_name_field)
        last_name_element.clear()
        last_name_element.send_keys(self.config.get('checkout_data', 'last_name'))
        
        # Fill street address
        street_element = self.web_utils.find_element(*self.street_address_field)
        street_element.clear()
        street_element.send_keys(self.config.get('checkout_data', 'street_address'))
        
        # Fill city
        city_element = self.web_utils.find_element(*self.city_field)
        city_element.clear()
        city_element.send_keys(self.config.get('checkout_data', 'city'))
        
        # Select state
        state_element = self.web_utils.find_element(*self.state_field)
        state_element.click()
        state_dropdown = self.web_utils.find_elements(*self.state_dropdown, retries=5)
        if state_dropdown:
            self.web_utils.safe_click(state_dropdown[0])
        
        # Fill postal code
        postal_element = self.web_utils.find_element(*self.postal_code_field)
        postal_element.clear()
        postal_element.send_keys(self.config.get('checkout_data', 'postal_code'))
        
        # Fill phone number
        phone_element = self.web_utils.find_element(*self.phone_field)
        phone_element.clear()
        phone_element.send_keys(self.config.get('checkout_data', 'phone_number'))
        
        time.sleep(2)  # Allow form to process
    
    def select_shipping_method(self):
        """Select first available shipping method"""
        time.sleep(2)  # Wait for shipping methods to load
        shipping_methods = self.web_utils.find_elements(*self.shipping_methods, retries=5)
        if shipping_methods:
            self.web_utils.safe_click(shipping_methods[0])
        time.sleep(2)
    
    def continue_to_payment(self):
        """Continue to payment section"""
        next_btn = self.web_utils.find_element(*self.next_button, retries=5)
        self.web_utils.safe_click(next_btn)
        time.sleep(3)
    
    def select_payment_method(self):
        """Select first available payment method"""
        payment_methods = self.web_utils.find_elements(*self.payment_methods, retries=5)
        if payment_methods:
            self.web_utils.safe_click(payment_methods[0])
        time.sleep(2)
    
    def place_order(self):
        """Place the order"""
        place_order_btn = self.web_utils.find_element(*self.place_order_button, retries=10)
        self.web_utils.safe_click(place_order_btn)
        time.sleep(5)  # Wait for order processing
    
    def verify_order_success(self):
        """Verify that order was placed successfully"""
        try:
            success_element = self.web_utils.find_element(*self.success_message, retries=10)
            return True
        except:
            try:
                confirmation_element = self.web_utils.find_element(*self.order_confirmation_message, retries=5)
                return True
            except:
                return False
    
    def get_order_number(self):
        """Get the order number from confirmation page"""
        try:
            confirmation_element = self.web_utils.find_element(*self.order_confirmation_message, retries=3)
            text = confirmation_element.text
            # Extract order number from text
            import re
            match = re.search(r'order number is:?\s*(\d+)', text, re.IGNORECASE)
            if match:
                return match.group(1)
        except Exception as e:
            logging.warning(f"Could not find order confirmation message or extract order number: {e}")
        return None 