# -*- coding: utf-8 -*-
"""
This module contains functions for performing
basic web related actions using Selenium WebDriver
Class:
    - WebUtils
        Properties;
           - driver
           - url
       Methods:
           - get
           - find_element
           - find_elements
           - find_element_by_id
           - find_elements_by_id
           - find_element_by_name
           - find_elements_by_name
           - find_element_by_xpath
           - find_elements_by_xpath
           - find_element_by_css_selector
           - find_elements_by_css_selector
           - find_element_by_class_name
           - find_elements_by_class_name
           - find_element_by_partial_link_text
           - find_element_by_link_text
           - wait_element_to_hide
           - switch_to_window
           - move_to
           - mouse_hover
"""
# pylint: disable=W0703
import logging
import os
import sys
import time
from bdb import BdbQuit
import inspect

import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as exp_cond


class WebUtils(object):
    """Class containing core functions for interacting with web pages"""
    url = None
    highlight_elements = False
    scrolling_area = (By.XPATH, "//div[contains(@class, 'scroll-wrapper')]/div")
    table = (By.XPATH, '//table')
    javascript_click = "arguments[0].click();"

    def __init__(self, driver):
        self.driver = driver
        if not os.environ.get('HIGHLIGHT_ELEMENTS', None):
            self.highlight_elements = True

    # pylint: disable=R0913
    def find_element(
            self, by_locator, locator, wait=1, retries=10,
            wait_for_clickable=True, log_errors=True, check_robust_xpath=True) -> WebElement:
        """Retrieves the first element found in driver's current page
        based on a specified locator, considering retry intervals
        to properly deal with page loading times"""
        element = None
        if by_locator == By.LINK_TEXT:
            element = self.find_element_by_link_text(locator, wait, retries, log_errors, check_robust_xpath)
        elif by_locator == By.ID:
            element = self.find_element_by_id(locator, wait, retries, wait_for_clickable, log_errors, check_robust_xpath)
        elif by_locator == By.NAME:
            element = self.find_element_by_name(locator, wait, retries, wait_for_clickable, log_errors, check_robust_xpath)
        elif by_locator == By.XPATH:
            element = self.find_element_by_xpath(locator, wait, retries, wait_for_clickable, log_errors, check_robust_xpath)
        elif by_locator == By.CLASS_NAME:
            element = self.find_element_by_class_name(locator, wait, retries, wait_for_clickable, log_errors, check_robust_xpath)
        elif by_locator == By.PARTIAL_LINK_TEXT:
            element = self.find_element_by_partial_link_text(locator, wait, retries, log_errors, check_robust_xpath)
        elif by_locator == By.CSS_SELECTOR:
            locator = locator.replace("\"", "'") \
                .replace("\'", "'") \
                .replace("\\'", "'")
            element = self.find_element_by_css_selector(locator, wait, retries, wait_for_clickable, log_errors, check_robust_xpath)
        else:
            for i in range(retries):
                try:
                    element = self.driver.find_element(by_locator, locator)
                    break
                except Exception as exception:
                    message = "Unable to find element with {}: '{}'." \
                              " Retry number: {} out of {}.".format(by_locator,
                                                                    locator,
                                                                    str(i + 1),
                                                                    str(retries))
                    if (i + 1) == retries:
                        raise exception
                    elif log_errors:
                        logging.info(message)
        return element

    def find_elements(self, by_locator, locator, wait=1, retries=8, log_errors=True) -> list[WebElement]:
        """Retrieves a list of all elements found in driver's current page
        based on a specified locator, considering retry intervals
        to properly deal with page loading times"""
        elements = None
        if by_locator == By.ID:
            elements = self.find_elements_by_id(locator, wait, retries, log_errors)
        elif by_locator == By.NAME:
            elements = self.find_elements_by_name(locator, wait, retries, log_errors)
        elif by_locator == By.XPATH:
            elements = self.find_elements_by_xpath(locator, wait, retries, log_errors)
        elif by_locator == By.CLASS_NAME:
            elements = self.find_elements_by_class_name(locator, wait, retries, log_errors)
        elif by_locator == By.CSS_SELECTOR:
            locator = locator.replace("\"", "'") \
                .replace("\'", "'") \
                .replace("\\'", "'")
            elements = self.find_elements_by_css_selector(locator, wait, retries, log_errors)
        else:
            for i in range(retries):
                try:
                    elements = self.driver.find_elements(by_locator, locator)
                    break
                except Exception as exception:
                    message = "Unable to find element with {}: '{}'." \
                              " Retry number: {} out of {}.".format(by_locator,
                                                                    locator,
                                                                    str(i + 1),
                                                                    str(retries))
                    if (i + 1) == retries:
                        raise exception
                    elif log_errors:
                        logging.info(message)
        return elements

    def find_element_by_id(self, element_id, wait=2, retries=8, wait_for_clickable=True, log_errors=True, check_robust_xpath=False):
        """Retrieves a web element using the ID locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if wait_for_clickable:
                    elem = wd_wait.until(
                        exp_cond.element_to_be_clickable((By.ID, element_id)))
                else:
                    elem = wd_wait.until(
                        exp_cond.presence_of_element_located((By.ID, element_id)))
                    elem = self.driver.find_element(By.ID, element_id)
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = "Unable to find element with id: '{}'. " \
                          "Retry number: {} out of {}.".format(element_id,
                                                               str(i + 1),
                                                               str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_elements_by_id(self, element_id, wait=1, retries=8, log_errors=True):
        """Retrieves all web elements found using the ID locator.
        Retries are implemented to properly deal with page loading times"""
        elements = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elements = wd_wait.until(
                    exp_cond.presence_of_all_elements_located(
                        (By.ID, element_id)))
                break
            except Exception as exception:
                message = "Unable to find elements with id: '{}'." \
                          " Retry number: {} out of {}.".format(element_id,
                                                                str(i + 1),
                                                                str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elements

    def find_element_by_name(self, name, wait=1, retries=8, wait_for_clickable=True, log_errors=True, check_robust_xpath=False):
        """Retrieves a web element using the NAME locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if wait_for_clickable:
                    elem = wd_wait.until(
                        exp_cond.element_to_be_clickable((By.NAME, name)))
                else:
                    elem = wd_wait.until(
                        exp_cond.presence_of_element_located((By.NAME, name)))
                    elem = self.driver.find_element(By.NAME, name)
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = "Unable to find element with name: '{}'." \
                          " Retry number: {} out of {}.".format(name,
                                                                str(i + 1),
                                                                str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_elements_by_name(self, name, wait=1, retries=8, log_errors=True):
        """Retrieves all web elements found using the NAME locator.
        Retries are implemented to properly deal with page loading times"""
        elements = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elements = wd_wait.until(
                    exp_cond.presence_of_all_elements_located((By.NAME, name)))
                break
            except Exception as exception:
                message = "Unable to find elements with name: '{}'." \
                          " Retry number: {} out of {}.".format(name,
                                                                str(i + 1),
                                                                str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elements

    def find_element_by_xpath(self, xpath, wait=10, retries=8, wait_for_clickable=True, log_errors=True, check_robust_xpath=False):
        """Retrieves a web element using the XPATH locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if wait_for_clickable:
                    elem = wd_wait.until(
                        exp_cond.element_to_be_clickable((By.XPATH, xpath)))
                else:
                    elem = wd_wait.until(
                        exp_cond.presence_of_element_located((By.XPATH, xpath)))
                    elem = self.driver.find_element(By.XPATH, xpath)
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = "Unable to find element with xpath: '{}'. " \
                          "Retry number: {} out of {}.".format(xpath.encode('utf8'),
                                                               str(i + 1),
                                                               str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_elements_by_xpath(self, xpath, wait=1, retries=8, log_errors=True):
        """Retrieves all web elements found using the XPATH locator.
        Retries are implemented to properly deal with page loading times"""
        elements = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elements = wd_wait.until(
                    exp_cond.presence_of_all_elements_located(
                        (By.XPATH, xpath)))
                break
            except Exception as exception:
                message = "Unable to find element with xpath: '{}'." \
                          " Retry number: {} out of {}.".format(xpath.encode('utf8'),
                                                                str(i + 1),
                                                                str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elements

    def find_element_by_css_selector(self, css, wait=1, retries=8, wait_for_clickable=True, log_errors=True, check_robust_xpath=False):
        """Retrieves a web element using the CSS selector locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if wait_for_clickable:
                    elem = wd_wait.until(
                        exp_cond.element_to_be_clickable((By.CSS_SELECTOR, css)))
                else:
                    elem = wd_wait.until(
                        exp_cond.presence_of_element_located((By.CSS_SELECTOR, css)))
                    elem = self.driver.find_element(By.CSS_SELECTOR, css)
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = "Unable to find element with css selector: '{}'." \
                          " Retry number: {} out of {}.".format(css.encode('utf8'),
                                                                str(i + 1),
                                                                str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_elements_by_css_selector(self, css, wait=1, retries=8, log_errors=True):
        """Retrieves all web elements found using the CSS SELECTOR locator.
        Retries are implemented to properly deal with page loading times"""
        elements = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elements = wd_wait.until(
                    exp_cond.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, css)))
                break
            except Exception as exception:
                message = "Unable to find element with css selector: '{}'." \
                          " Retry number: {} out of {}.".format(css.encode('utf8'),
                                                                str(i + 1),
                                                                str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elements

    def find_element_by_class_name(self, class_name, wait=1, retries=8, wait_for_clickable=True, log_errors=True, check_robust_xpath=False):
        """Retrieves a web element using the CLASS NAME locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if wait_for_clickable:
                    elem = wd_wait.until(
                        exp_cond.element_to_be_clickable((By.CLASS_NAME, class_name)))
                else:
                    elem = wd_wait.until(
                        exp_cond.presence_of_element_located((By.CLASS_NAME, class_name)))
                    elem = self.driver.find_element(By.CLASS_NAME, class_name)
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = "Unable to find element with class name: '{}'." \
                          " Retry number: {} out of {}.".format(class_name.encode('utf8'),
                                                                str(i + 1),
                                                                str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_elements_by_class_name(self, class_name, wait=1, retries=8, log_errors=True):
        """Retrieves all web elements found using the CLASS NAME locator.
        Retries are implemented to properly deal with page loading times"""
        elements = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elements = wd_wait.until(
                    exp_cond.presence_of_all_elements_located(
                        (By.CLASS_NAME, class_name)))
                break
            except Exception as exception:
                message = "Unable to find element with css selector: '{}'." \
                          " Retry number: {} out of {}.".format(class_name.encode('utf8'),
                                                                str(i + 1),
                                                                str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elements

    def find_element_by_partial_link_text(self, partial_link_text, wait=1, retries=8, log_errors=True, check_robust_xpath=False):
        """Retrieves a web element using the PARTIAL LINK TEXT locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                elem = wd_wait.until(
                    exp_cond.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, partial_link_text)) and
                    exp_cond.visibility_of_element_located((By.PARTIAL_LINK_TEXT, partial_link_text)) and
                    exp_cond.element_to_be_clickable((By.PARTIAL_LINK_TEXT, partial_link_text)))
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = "Unable to find element with partial link text containing: '{}'." \
                          " Retry number: {} out of {}.".format(partial_link_text.encode('utf8'),
                                                                str(i + 1),
                                                                str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def find_element_by_link_text(self, text, wait=1, retries=8, log_errors=True, check_robust_xpath=False):
        """Retrieves a web element using the LINK TEXT locator.
        Retries are implemented to properly deal with page loading times"""
        elem = None
        for i in range(retries):
            try:
                wd_wait = ui.WebDriverWait(self.driver, int(wait))
                if i % 2 == 0:
                    elem = wd_wait.until(
                        exp_cond.element_to_be_clickable((By.LINK_TEXT, text)))
                else:
                    elem = wd_wait.until(exp_cond.element_to_be_clickable(
                        (By.XPATH, "//a[text()='" + text + "']")))
                if self.highlight_elements:
                    highlight(elem)
                break
            except Exception as exception:
                message = "Unable to find element with link text: '{}'." \
                          " Retry number: {} out of {}.".format(text,
                                                                str(i + 1),
                                                                str(retries))
                if (i + 1) == retries:
                    raise exception
                elif log_errors:
                    logging.info(message)
        return elem

    def wait_element_to_hide(self, by_locator, locator, wait=1, retries=8):
        for i in range(retries):
            # noinspection PyBroadException
            try:
                self.driver.find_element(by_locator, locator)
                time.sleep(wait)
            except:
                return
        raise Exception("Element is still visible: {}:{}".format(by_locator, locator))

    def wait_for_element_to_be_clickable(self, by_locator, locator, wait=3, retries=3):
        for i in range(retries):
            # noinspection PyBroadException
            try:
                ui.WebDriverWait(self.driver, wait).until(exp_cond.element_to_be_clickable((by_locator, locator)))
            except:
                return
        raise Exception("Element is not clickable: {}:{}".format(by_locator, locator))

    def get(self, url, wait_for_page_load=False):
        """Go to the specified url """
        self.driver.get(url)
        if wait_for_page_load:
            wdwait = ui.WebDriverWait(self.driver, 10)
            wdwait.until(lambda d: d.execute_script("return document.readyState") in ["interactive", "complete"])

    def move_to(self, element, x_offset=0, y_offset=0, show_element_at_top=True):
        show_at_top = "true" if show_element_at_top else "false"
        self.driver.execute_script("arguments[0].scrollIntoView({});".format(show_at_top), element)
        self.mouse_hover(element, x_offset, y_offset)

    def scroll_to_top_of_element(self, element, pixels=500):
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(self.get_platform_dependent_ctrl_key() + Keys.HOME)
        self.driver.execute_script("arguments[0].scrollTop = {};".format(pixels), element)

    def scroll_to_top_of_page(self):
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(self.get_platform_dependent_ctrl_key() + Keys.HOME)

    def scroll_to_top_of_table(self):
        logging.info("Scrolling to top of table")
        table_element = self.find_element(*self.table)
        self.driver.execute_script("arguments[0].scrollIntoView({alignToTop : 'true'});", table_element)
        time.sleep(1)

    def scroll_to_bottom_of_element(self, element):
        logging.info("Scrolling to top of element")
        self.driver.execute_script("arguments[0].scrollIntoView({alignToTop : 'false'});", element)
        time.sleep(1)

    def perform_table_scroll_left(self, offset=0):
        scrolling_area_elem = self.find_elements(*self.scrolling_area)[-1]
        self.mouse_hover(scrolling_area_elem)
        if offset == 0:
            self.driver.execute_script("arguments[0].scrollLeft -= arguments[0].scrollWidth", scrolling_area_elem)
        else:
            self.driver.execute_script("arguments[0].scrollLeft -= {}".format(offset), scrolling_area_elem)

    def mouse_hover(self, element, x_offset=0, y_offset=0):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).move_by_offset(x_offset, y_offset).perform()

    def mouse_hover_with_offset(self, element, x_offset=0, y_offset=0):
        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(element, x_offset, y_offset).perform()

    def switch_to_window(self, partial_page_url):
        # original_page_handle = self.driver.window_handles[0]
        matching_window_handler = None
        for i in range(10):
            window_handles = self.driver.window_handles
            if len(window_handles) > 1:
                for window_handler in self.driver.window_handles:
                    self.driver.switch_to.window(window_handler)
                    page_url = self.driver.current_url
                    if partial_page_url in page_url:
                        matching_window_handler = window_handler
                        logging.info("Pop-up page with partial URL {} was found...".format(partial_page_url))
                        break
            if matching_window_handler:
                break
            time.sleep(1)
        if not matching_window_handler:
            raise Exception("It was not possible to find a window with partial url '{}'".format(partial_page_url))
        return matching_window_handler

    def safe_click(self, element, javascript_only=False):
        """
        Performs a click on a web element in a robust manner.
        This method first attempts a normal click on the element. If an ElementClickInterceptedException is raised,
        it tries to click on the element using JavaScript.
        Args:
            element: selenium webelement.
        """
        if javascript_only:
            try:
                # Attempt a javascript click
                self.driver.execute_script(self.javascript_click, element)
            except Exception as ex:
                logging.error(f"Failed to click on element: {element}. Error: {ex}")
                raise ex
        else:
            try:
                # Attempt a normal click
                element.click()
            except Exception:
                # If the click is intercepted, try using JavaScript
                try:
                    self.driver.execute_script(self.javascript_click, element)
                except Exception as inner_ex:
                    logging.error(f"Failed to click on element: {element}. Error: {inner_ex}")
                    raise inner_ex


    def is_element_displayed(self, element_locator):
        retries = 2
        for i in range(retries):
            try:
                self.find_element(*element_locator, wait_for_clickable=False, retries=1, log_errors=False)
                return True
            except (NoSuchElementException, TimeoutException):
                if i == retries - 1:
                    return False
                time.sleep(1)
        return False

    @staticmethod
    def get_platform_dependent_ctrl_key():
        ctrl_key = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
        return ctrl_key


def highlight(element, color="blue", border=3):
    """Highlights (blinks) a Selenium Webdriver element"""
    # noinspection PyProtectedMember
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
    apply_style("border: {0}px solid {1};".format(border, color))


def retry(retry_count=3, retry_interval=2):
    """
    retry decorator

    Example:
    @retry(3, 2) or @retry()
    def test():
        pass
    """

    def real_decorator(decor_method):
        def wrapper(*args, **kwargs):
            for count in range(retry_count):
                try:
                    if "is_retry" in inspect.getfullargspec(decor_method).args and count > 0:
                        kwargs["is_retry"] = True
                    return_values = decor_method(*args, **kwargs)
                    return return_values
                except (SystemExit, BdbQuit, KeyboardInterrupt):
                    print("Exiting the program due to the following exception: {}".format(sys.exc_info()))
                    try:
                        sys.exit(130)
                    except SystemExit:
                        os._exit(130)
                except StopExecutionException as error:
                    raise error
                except Exception as error:
                    # On exception, retry till retry_frequency is exhausted
                    error_msg = "RETRYING ON ERROR (%s). Function execution failed for %s.%s" % (count + 1,
                                                                                                 decor_method.__module__,
                                                                                                 decor_method.__name__)
                    # print(error_msg)
                    logging.warning(error_msg)
                    # sleep for retry_interval
                    time.sleep(retry_interval)
                    # If the retries are exhausted, raise the exception
                    if count == retry_count - 1:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        current_tb = exc_tb
                        first_tb = None
                        while hasattr(current_tb, 'tb_next'):
                            curr_exc_module = current_tb.tb_frame.f_code.co_filename
                            if "features" in curr_exc_module and \
                                    "steps" in curr_exc_module and \
                                    "web_utils" not in curr_exc_module:
                                first_tb = current_tb
                            current_tb = current_tb.tb_next
                        if first_tb:
                            exc_module = first_tb.tb_frame.f_code.co_filename
                            exc_method = first_tb.tb_frame.f_code.co_name
                            exc_line = first_tb.tb_frame.f_lineno
                            logging.warning("Retries limit has been reached.")
                            logging.warning("\n-MODULE: '{}'\n-METHOD: '{}'\n-LINE:'{}'\n-EXCEPTION: {}".format(exc_module,
                                                                                                                exc_method,
                                                                                                                exc_line,
                                                                                                                str(exc_obj)))
                        raise error
        return wrapper

    return real_decorator


def retry_function(return_value_on_failure,
                   retry_message: str = None,
                   retries: int = 5,
                   wait: int = 1,
                   wait_spinning_wheel_on_retry: bool = False,
                   wait_spinning_wheel_on_retry_number: int = 2):

    if not retry_message:
        retry_message = "Retrying in {} seconds...".format(wait)

    def real_decorator(decor_method):
        def wrapper(*args, **kwargs):
            for i in range(1, retries + 1):
                try:
                    return decor_method(*args, **kwargs)
                except (SystemExit, BdbQuit, KeyboardInterrupt):
                    print("Exiting the program due to the following exception: {}".format(sys.exc_info()))
                    try:
                        sys.exit(130)
                    except SystemExit:
                        os._exit(130)
                except:
                    if wait_spinning_wheel_on_retry and i == wait_spinning_wheel_on_retry_number:
                        module_instance = None
                        for argument in args:
                            module_instance = argument
                            break
                        if module_instance:
                            module_instance.wait_spinning_wheel_to_hide()
                    if i == retries:
                        # if return_value_on_failure is instance of Exception, raise it
                        if isinstance(return_value_on_failure, Exception):
                            raise return_value_on_failure
                        else:
                            return return_value_on_failure
                    else:
                        logging.info(retry_message)
                        time.sleep(wait)
        return wrapper
    return real_decorator


def wait_and_close_adds_popups(selenium_driver, wait_for_ad_blocker=False):
    """Wait for and close ads and popups"""
    try:
        # Wait for 5 seconds until #google_vignette is present in current url
        if wait_for_ad_blocker:
            wait = ui.WebDriverWait(selenium_driver, 5)
            wait.until(exp_cond.url_contains('#google_vignette'))
        
        if "#google_vignette" in selenium_driver.current_url:
            try:
                selenium_driver.execute_script("""
                    const elements = document.getElementsByClassName("google-auto-placed");
                    while (elements.length > 0) elements[0].remove();
                """)
                time.sleep(1)
                selenium_driver.execute_script("""
                    const elements = document.getElementsByClassName("adsbygoogle adsbygoogle-noablate");
                    while (elements.length > 0) elements[0].remove();
                """)
                logging.info("Ad elements removed successfully")
                return True
            except Exception as e:
                logging.info(f"Error removing ad elements: {e}")
                
    except Exception as e:
        logging.info(f"Error removing ad elements: {e}")
        logging.info("No Google Vignette ad detected within 5 seconds, continuing without ad dismissal")
    return False

class StopExecutionException(Exception):
    pass 