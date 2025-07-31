"""
Checkout step definitions - Core Requirements Only
"""
import time
import logging
from behave import step, then
from features.steps.pages.checkout_page import CheckoutPage as CHP
from features.steps.pages.cart_page import CartPage as CP


@step('I open the shopping cart page')
def step_given_on_cart_page(context):
    """Navigate to shopping cart page"""
    # Assume we're coming from a product page
    if hasattr(context.current_page, 'open_cart_page'):
        context.current_page = context.current_page.open_cart_page()
    else:
        # Fallback: create cart page directly
        context.current_page = CP(context.browser.driver)
    time.sleep(2)


@step('I proceed to checkout')
def step_when_proceed_to_checkout(context):
    """Proceed to checkout from cart page"""
    cart_page: CP = context.current_page
    context.current_page = cart_page.proceed_to_checkout()
    time.sleep(3)

@step('I fill out all required shipping information if not already set')
def step_when_fill_shipping_info_dummy(context):
    """Fill shipping information with dummy data from config"""
    checkout_page: CHP = context.current_page
    if not checkout_page.is_address_already_filled():
        # Get all configuration data
        first_name = checkout_page.config.get('checkout_data', 'first_name')
        last_name = checkout_page.config.get('checkout_data', 'last_name')
        street_address = checkout_page.config.get('checkout_data', 'street_address')
        city = checkout_page.config.get('checkout_data', 'city')
        postal_code = checkout_page.config.get('checkout_data', 'postal_code')
        phone_number = checkout_page.config.get('checkout_data', 'phone_number')
        
        # Pass all data as arguments to the method
        checkout_page.fill_shipping_information(
            first_name, last_name, street_address, city, postal_code, phone_number
        )
    else:
        logging.info("Shipping information is already set. so the default shipping address will be used.")


@step('I select a shipping method')
def step_when_select_shipping_method(context):
    """Select a shipping method"""
    checkout_page: CHP = context.current_page
    checkout_page.select_shipping_method()


@step('I continue to payment section')
def step_when_continue_to_payment(context):
    """Continue to payment section"""
    checkout_page: CHP = context.current_page
    checkout_page.continue_to_payment()


@step('I select a payment method')
def step_when_select_payment_method(context):
    """Select a payment method"""
    checkout_page: CHP = context.current_page
    checkout_page.select_payment_method()


@step('I place the order')
def step_when_place_order(context):
    """Place the order"""
    checkout_page: CHP = context.current_page
    checkout_page.place_order()


@then('I should see the order confirmation page')
def step_then_see_order_confirmation(context):
    """Verify order confirmation page is displayed"""
    checkout_page: CHP = context.current_page
    assert checkout_page.verify_order_success(), "Order confirmation not displayed"


@then('I should see the order number displayed')
def step_then_see_order_number(context):
    """Verify order number is displayed"""
    checkout_page: CHP = context.current_page
    order_number = checkout_page.get_order_number()
    assert order_number is not None, "Order number not displayed"
    context.order_number = order_number 