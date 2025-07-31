"""
Cart Page Object Model for Magento E-commerce
"""
import logging
import time
from selenium.webdriver.common.by import By
from features.steps.pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage(BasePage):
    """Shopping cart page object model"""
    
    # Cart page locators
    cart_items = (By.XPATH, "//tbody[@class='cart item']")
    product_name = (By.XPATH, ".//strong[@class='product-item-name']//a")
    product_price = (By.XPATH, ".//span[@class='cart-price']//span[@class='price']")
    product_quantity = (By.XPATH, ".//input[contains(@class,'qty')]")
    
    # Cart summary locators
    subtotal = (By.XPATH, "//div[@class='cart-summary']//tr[contains(@class, 'sub')]//span[@class='price']")
    
    # Cart action buttons
    proceed_to_checkout_button = (By.XPATH, "//button[@data-role='proceed-to-checkout']")
    continue_shopping_link = (By.XPATH, "//a[contains(@class,'continue')]")
    delete_cart_item_buttons = (By.XPATH, "//a[contains(@class,'action-delete')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.url_contains('/checkout/'))        
    
    def get_cart_items(self):
        """Get list of items in the cart"""
        items = []
        try:
            cart_items = self.web_utils.find_elements(*self.cart_items)
            
            for item in cart_items:
                try:
                    name_element = item.find_element(*self.product_name)
                    price_element = item.find_element(*self.product_price)
                    qty_element = item.find_element(*self.product_quantity)
                    
                    items.append({
                        'name': name_element.text,
                        'price': price_element.text,
                        'quantity': int(qty_element.get_attribute('value'))
                    })
                except Exception as e:
                    logging.warning(f"Could not extract information from cart item: {e}")
                    continue
                    
        except Exception as e:
            logging.info("No cart items found or cart is empty")
        
        return items
    
    def get_cart_summary(self):
        """Get cart totals summary"""
        summary = {}
        
        try:
            subtotal_element = self.web_utils.find_element(*self.subtotal, retries=3)
            summary['subtotal'] = subtotal_element.text
        except:
            summary['subtotal'] = "N/A"
               
        return summary
    
    
    def proceed_to_checkout(self):
        """Proceed to checkout from cart page - returns CheckoutPage"""
        checkout_btn = self.web_utils.find_element(*self.proceed_to_checkout_button)
        self.web_utils.safe_click(checkout_btn)
        
        # Import here to avoid circular imports
        from features.steps.pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)
    
    def continue_shopping(self):
        """Continue shopping from cart page - returns HomePage"""
        continue_btn = self.web_utils.find_element(*self.continue_shopping_link)
        self.web_utils.safe_click(continue_btn)
        
        # Import here to avoid circular imports
        from features.steps.pages.homepage import HomePage
        return HomePage(self.driver) 

    def empty_cart(self):
        """Empty cart"""
        delete_cart_item_buttons = self.web_utils.find_elements(*self.delete_cart_item_buttons)
        for _ in range(len(delete_cart_item_buttons)):
            delete_cart_item_button = self.web_utils.find_element(*self.delete_cart_item_buttons)
            self.web_utils.safe_click(delete_cart_item_button)
            time.sleep(1)
        time.sleep(1)