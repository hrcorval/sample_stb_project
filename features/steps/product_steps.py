"""
Product browsing step definitions - Core Requirements Only
"""
import logging
import time
from behave import step, then
from features.steps.pages.homepage import HomePage as HP
from features.steps.pages.product_page import ProductPage as PP
from features.steps.pages.cart_page import CartPage as CP
from features.steps.pages.base_page import BasePage
from features.steps.pages.web_utils import retry, wait_and_close_adds_popups


@step('I open the homepage')
def step_given_on_homepage(context):
    """Navigate to homepage and set as current page"""
    context.current_page = HP(context.browser.driver)
    context.current_page.navigate_to_homepage()
    assert context.current_page.verify_page_loaded(), "Homepage did not load correctly"


@step('I navigate to the product listing page')
def step_when_navigate_to_product_listing(context):
    """Navigate to product listing page from current page"""
    home_page: HP = context.current_page
    context.current_page = home_page.open_product_page()


@step('I select the {elem_index:d}st item from the listed products')
@step('I select the {elem_index:d}nd item from the listed products')
@step('I select the {elem_index:d}rd item from the listed products')
@step('I select the {elem_index:d}th item from the listed products')
@retry()
def step_when_select_a_product_by_index(context, elem_index):
    """Select product by ordinal index (1st, 2nd, 3rd, etc.)"""
    product_page: PP = context.current_page
    # Convert from 1-based ordinal to 0-based index
    zero_based_index = elem_index - 1
    context.selected_product_name = product_page.click_product_by_index(zero_based_index)

@step('I select the "{categories}" product category')
@step('I select the "{categories}" product categories')
@retry()
def step_when_select_a_category(context, categories):
    """Select category"""
    current_page: BasePage = context.current_page
    categories_list = categories.split(" - ")
    retries = 2
    for _ in range(retries):
        product_page = current_page.select_product_categories_from_top_menu(categories_list)
        if not wait_and_close_adds_popups(context.browser.driver):
            break
    context.current_page = product_page

@step('I configure product options with the following data')
@retry()
def step_when_configure_product_options(context):
    """Configure product options"""
    product_page: PP = context.current_page
    product_size = context.table.rows[0]['size']
    product_color = context.table.rows[0]['color']
    product_quantity = context.table.rows[0]['quantity']
    try:
        product_page.select_product_size(size=product_size)
    except:
        logging.info("Product size option not available or could not be selected")
    try:
        product_page.select_product_color(color=product_color)
    except:
        logging.info("Product color option not available or could not be selected")
    try:
        product_page.select_product_quantity(quantity=product_quantity)
    except:
        logging.info("Product quantity option not available or could not be selected")


@step('I add the product to cart')
@retry()
def step_when_add_product_to_cart(context):
    """Add product to cart"""
    if "products_added_to_cart" not in context:
        context.products_added_to_cart = []
    product_page: PP = context.current_page
    product_data = product_page.add_product_to_cart()
    logging.info(f"The following product was added to cart: {product_data}")
    context.products_added_to_cart.append(product_data)


@step('I navigate back to product listing')
def step_when_navigate_back_to_listing(context):
    """Navigate back to product listing"""
    product_page: PP = context.current_page
    context.current_page = product_page.go_back_to_product_listing()


@step('I navigate to the shopping cart page')
def step_when_navigate_to_cart(context):
    """Navigate to shopping cart page"""
    product_page: PP = context.current_page
    context.current_page = product_page.open_cart_page()


@then('I should see a success message')
def step_then_see_success_message(context):
    """Verify success message"""
    product_page: PP = context.current_page
    success = product_page.verify_add_to_cart_success()
    assert success, "Success message not displayed after adding product to cart"

