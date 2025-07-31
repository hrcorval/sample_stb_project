"""
Behave environment file with hooks for test automation
"""
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from behavex_images import image_attachments
from features.steps.pages.web_utils import wait_and_close_adds_popups
import SeleniumAdblock



class Browser:
    """Browser management class"""
    def __init__(self, driver):
        self.driver = driver


def before_all(context):
    """before_all behave hook"""
    context.dry_run = True if os.environ.get("DRY_RUN", None) else False
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting test automation framework...")
    image_attachments.set_attachments_condition(context, image_attachments.AttachmentsCondition.ALWAYS)


def before_feature(context, feature):
    """before_feature behave hook"""
    logging.info(f"Starting feature: {feature.name}")


def before_scenario(context, scenario):
    """before_scenario behave hook"""
    logging.info(f"Starting scenario: {scenario.name}")
    # Set up browser with comprehensive ad blocking
    chrome_options = SeleniumAdblock.SeleniumAdblock()._startAdBlock()
    # chrome_options = ChromeOptions()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    
    # Basic browser options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
       
    context.browser = Browser(driver)


def before_step(context, step):
    """before_step behave hook"""
    logging.info("-"*40)
    logging.info("STEP: {}".format(step.name))
    if "browser" in context:
        wait_and_close_adds_popups(context.browser.driver)

def after_step(context, step):
    """after_step behave hook"""
    if "browser" in context:
        try:
            screenshot_as_png = context.browser.driver.get_screenshot_as_png()
            image_attachments.attach_image_binary(context, screenshot_as_png)
        except Exception as ex:
            logging.warning("It was not possible to attach the screenshot: {}".format(ex))

def after_scenario(context, scenario):
    """after_scenario behave hook"""
    logging.info(f"Completed scenario: {scenario.name}")
    # Clean up browser
    if hasattr(context, 'browser') and context.browser:
        try:
            context.browser.driver.quit()
        except:
            logging.debug("Browser was already closed...")
        context.browser = None


def after_feature(context, feature):
    """after_feature behave hook"""
    logging.info(f"Completed feature: {feature.name}")


def after_all(context):
    """after_all behave hook"""
    logging.info("Test automation framework completed.") 