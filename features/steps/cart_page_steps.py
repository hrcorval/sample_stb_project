"""
Product browsing step definitions - Core Requirements Only
"""
import logging
import time
from behave import step, then
from features.steps.pages.cart_page import CartPage as CP
from features.steps.pages.base_page import BasePage


@then('the cart counter should be updated')
def step_then_cart_counter_updated(context):
    """Verify cart counter is updated"""
    if hasattr(context.current_page, 'get_cart_counter'):
        cart_count = context.current_page.get_cart_counter()
        logging.info(f"Cart counter is updated to {cart_count}")
        assert cart_count > 0, "Cart counter was not updated"
    else:
        raise AssertionError(f"Current page {type(context.current_page).__name__} does not support cart counter")


@then('the cart counter should show "{count}" items')
def step_then_cart_counter_shows_count(context, count):
    """Verify specific cart count"""
    expected_count = int(count)
    cart_count = context.current_page.get_cart_counter()
    logging.info(f"Cart counter shows {cart_count}, expected {expected_count}")
    assert cart_count == expected_count, f"Cart counter shows {cart_count}, expected {expected_count}"


@then('I should see the correct product names, quantities and prices in my cart')
def step_then_see_correct_products_in_cart(context):
    """Verify correct products are in cart"""
    cart_page: CP = context.current_page
    cart_items = cart_page.get_cart_items()
    products_added_to_cart = context.products_added_to_cart
    for item_index in range(len(products_added_to_cart)):
        # it is expected that the order of products in the cart is the same as the order of products added to the cart
        assert products_added_to_cart[item_index]['name'] == cart_items[item_index]['name'], f"Product {context.products_added_to_cart[item_index]['name']} not found in cart"
        assert products_added_to_cart[item_index]['quantity'] == cart_items[item_index]['quantity'], f"Product {context.products_added_to_cart[item_index]['name']} quantity {context.products_added_to_cart[item_index]['quantity']} does not match cart quantity {cart_items[item_index]['quantity']}"
        assert products_added_to_cart[item_index]['price'] == cart_items[item_index]['price'], f"Product {context.products_added_to_cart[item_index]['name']} price {context.products_added_to_cart[item_index]['price']} does not match cart price {cart_items[item_index]['price']}"
    assert len(cart_items) > 0, "No products found in cart"


@then('I should see the correct order total calculations')
def step_then_see_correct_totals(context):
    """Verify order total calculations are correct"""
    cart_page: CP = context.current_page
    cart_subtotal_amount = float(cart_page.get_cart_summary()['subtotal'].replace("$", ""))
    sum_of_product_prices = sum(float(product['price'].replace("$", "")) * product['quantity'] for product in context.products_added_to_cart)
    logging.info(f"Cart subtotal amount {cart_subtotal_amount}, sum of product prices {sum_of_product_prices}")
    assert cart_subtotal_amount == sum_of_product_prices, f"Cart subtotal amount {cart_subtotal_amount} does not match sum of product prices {sum_of_product_prices}"


@step('I remove all the products from the shopping cart if it is not empty')
def step_then_empty_cart(context):
    """Empty shopping cart if it is not empty"""
    current_page: BasePage = context.current_page
    if current_page.get_cart_counter() > 0:
        cart_page: CP = current_page.open_cart_page()
        context.current_page = cart_page
        if cart_page.get_cart_items():
            cart_page.empty_cart()