#!/usr/bin/python3
# -*- encoding=utf8 -*-

import time
from termcolor import colored

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys


class WebElement(object):
    _locator = ()
    _web_driver = None
    _page = None
    _timeout = 10
    _wait_after_click = False  # TODO: how we can wait after click?

    def __init__(self, how, what, timeout=15, wait_after_click=False, **kwargs):
        self._timeout = timeout
        self._wait_after_click = wait_after_click
        self._locator = (how, what)

        # for attr in kwargs:
        #     self._locator = (str(attr).replace('_', ' '), str(kwargs.get(attr)))

    def find(self, timeout=15.0):
        """ Find element on the page. """

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                ec.presence_of_element_located(self._locator)
            )
        except:
            print(colored('Element not found on the page!', 'red'))

        return element

    def wait_to_be_clickable(self, timeout=15.0, check_visibility=True):
        """ Wait until the element will be ready for click. """

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                ec.element_to_be_clickable(self._locator)
            )
        except:
            print(colored('Element not clickable!', 'red'))

        if check_visibility:
            self.wait_until_not_visible()

        return element

    def wait_to_not_be_clickable(self, timeout=15.0):
        """ Wait until the element is not clickable. """

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                ec.element_to_be_clickable(self._locator)
            )
        except:
            pass

        return element

    def is_clickable(self):
        """ Check is element ready for click or not. """

        element = self.wait_to_be_clickable(timeout=0.1)
        return element is not None

    def is_not_clickable(self):
        """ Check is element is not clickable. """

        element = self.wait_to_not_be_clickable(timeout=0.1)
        return element is None

    def is_presented(self):
        """ Check that element is presented on the page. """

        element = self.find(timeout=0.1)
        return element is not None

    def is_not_presented(self, timeout=0.1):
        """ Check that element is not presented on the page. """

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                ec.presence_of_element_located(self._locator)
            )
            if element:
                return False
        except:
            return True

    def is_visible(self, timeout=0.1):
        """ Check that element is not presented on the page. """

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                ec.visibility_of_element_located(self._locator)
            )
            if element:
                return True
        except:
            return False

    def is_not_visible(self, timeout=0.1):
        """ Check that element is not presented on the page. """

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                ec.visibility_of_element_located(self._locator)
            )
            if element:
                return False
        except:
            return True

    def wait_until_not_visible(self, timeout=10):

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                ec.visibility_of_element_located(self._locator)
            )
        except:
            print(colored('Element not visible!', 'red'))

        if element:
            js = ('return (!(arguments[0].offsetParent === null) && '
                  '!(window.getComputedStyle(arguments[0]) === "none") &&'
                  'arguments[0].offsetWidth > 0 && arguments[0].offsetHeight > 0'
                  ');')
            visibility = self._web_driver.execute_script(js, element)
            iteration = 0

            while not visibility and iteration < 10:
                time.sleep(0.5)

                iteration += 1

                visibility = self._web_driver.execute_script(js, element)
                print('Element {0} visibility: {1}'.format(self._locator, visibility))

        return element

    def send_keys(self, keys, click=True, clear=True, wait=1):
        """ Send keys to the element. """

        keys = keys.replace('\n', '\ue007')

        element = self.wait_to_be_clickable()

        if element:
            if click:
                element.click()
            if clear:
                element.clear()
            element.send_keys(keys)
            time.sleep(wait)
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

    # def js_send_keys(self, value):
    #     """ Send keys by js script. """
    #
    #     element = self.find()
    #
    #     self._web_driver.execute_script(f"arguments[0].setAttribute('value', '{value}')", element)

    def js_click(self):
        """ Click by js script. """

        element = self.find()

        self._web_driver.execute_script(f"arguments[0].click()", element)

    def clear(self):
        """ Clear field. """

        element = self.wait_to_be_clickable()

        if element:
            element.click()
            element.clear()
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

    def get_text(self):
        """ Get alert_text of the element. """

        element = self.find()
        text = ''

        try:
            text = str(element.text)
        except Exception as e:
            print('Error: {0}'.format(e))

        return text

    def get_attribute(self, attr_name):
        """ Get attribute of the element. """

        element = self.find()

        if element:
            return element.get_attribute(attr_name)

    def _set_value(self, value, clear=False):
        """ Set value to the input element. """

        element = self.find()

        if clear:
            element.clear()

        element.send_keys(value)

    def click(self, hold_seconds=0, x_offset=1, y_offset=1):
        """ Wait and click the element. """

        element = self.wait_to_be_clickable()

        if element:
            action = ActionChains(self._web_driver)
            action.move_to_element_with_offset(element, x_offset, y_offset). \
                pause(hold_seconds).click(on_element=element).perform()
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

        if self._wait_after_click:
            self._page.wait_page_loaded()

    def right_mouse_click(self, x_offset=0, y_offset=0, hold_seconds=0):
        """ Click right mouse button on the element. """

        element = self.wait_to_be_clickable()

        if element:
            action = ActionChains(self._web_driver)
            action.move_to_element_with_offset(element, x_offset, y_offset). \
                pause(hold_seconds).context_click(on_element=element).perform()
        else:
            msg = 'Element with locator {0} not found'
            raise AttributeError(msg.format(self._locator))

    def highlight_and_make_screenshot(self, file_name='element.png'):
        """ Highlight element and make the screen-shot of all page. """

        element = self.find()

        # Scroll page to the element:
        self._web_driver.execute_script("arguments[0].scrollIntoView();", element)

        # Add red border to the style:
        self._web_driver.execute_script("arguments[0].style.border='3px solid red'", element)

        # Make screen-shot of the page:
        self._web_driver.save_screenshot(file_name)

    def scroll_to_element(self):
        """ Scroll page to the element. """

        element = self.find()

        # Scroll page to the element:
        # Option #1 to scroll to element:
        # self._web_driver.execute_script("arguments[0].scrollIntoView();", element)

        # Option #2 to scroll to element:
        try:
            element.send_keys(Keys.DOWN)
        except:
            pass  # Just ignore the error if we can't send the keys to the element

    def delete(self):
        """ Deletes element from the page. """

        element = self.find()

        # Delete element:
        self._web_driver.execute_script("arguments[0].remove();", element)

    # # # # # Troverlo methods

    def show_advanced_filters(self):

        element = self.wait_to_be_clickable()

        if "show_advanced_filters" in (str(element.get_attribute('class'))):
            element.click()

    def hide_advanced_filters(self):

        element = self.wait_to_be_clickable()

        if "hide_advanced_filters" in (str(element.get_attribute('class'))):
            element.click()

    # def input_to_list(self, alert_text):
    #
    #     list_input = '> div > div:nth-child(4) > div:nth-child(1) > div.p-multiselect-filter-container > input'
    #     list_first_item = ' > div > div:nth-child(4) > div:nth-child(2) > ul > p-multiselectitem:nth-child(1)'
    #     list_select_all_checkbox = ' > div > div:nth-child(4) > div:nth-child(1) > div'
    #
    #     element = self.wait_to_be_clickable()
    #
    #     element_attr_name = element.get_attribute('name')
    #
    #     element_input = WebDriverWait(self._web_driver, 0.1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[name="{element_attr_name}"]{list_input}')))
    #     element_input.send_keys(alert_text)
    #
    # def select_first_item(self):
    #
    #     list_first_item = ' > div > div:nth-child(4) > div:nth-child(2) > ul > p-multiselectitem:nth-child(1)'
    #     list_select_all_checkbox = ' > div > div:nth-child(4) > div:nth-child(1) > div'
    #
    #     element = self.wait_to_be_clickable()
    #
    #     element_attr_name = element.get_attribute('name')
    #
    #     element_first_item = WebDriverWait(self._web_driver, 0.1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[name="{element_attr_name}"]{list_first_item}')))
    #     element_first_item.click()

    def select_filter_value(self, text, timeout=15):
        """ Input and select first value from filter list"""

        input_locator = '> div > div:nth-child(4) > div:nth-child(1) > div.p-multiselect-filter-container > input'
        # first_item_locator = ' > div > div:nth-child(4) > div:nth-child(2) > ul > p-multiselectitem:nth-child(1)'
        found_item_locator = f'[aria-label="{text}"]'
        # select_all_checkbox_locator = ' > div > div:nth-child(4) > div:nth-child(1) > div'
        close_locator = ' > div > div:nth-child(4) > div:nth-child(1) > button'

        element = self.wait_to_be_clickable()
        element.click()

        filter_attr_name = f'[name="' + element.get_attribute('name') + '"]'

        # Input text to input field
        filter_input = WebDriverWait(self._web_driver, timeout).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, f'{filter_attr_name}{input_locator}')))
        filter_input.send_keys(text)

        # # Select first found item
        # filter_first_item = WebDriverWait(self._web_driver, timeout).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, f'[name="{filter_attr_name}"]{first_item_locator}')))
        # filter_first_item.click()

        # Select found item
        filter_found_item = WebDriverWait(self._web_driver, timeout).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, f'{filter_attr_name} {found_item_locator}')))
        filter_found_item.click()

        # Close filter list
        filter_close = WebDriverWait(self._web_driver, timeout).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, f'{filter_attr_name}{close_locator}')))
        filter_close.click()

# class ManyWebElements(WebElement):
#
#     def __getitem__(self, item):
#         """ Get list of elements and try to return required element. """
#
#         elements = self.find()
#         return elements[item]
#
#     def find(self, timeout=15):
#         """ Find elements on the page. """
#
#         elements = []
#
#         try:
#             elements = WebDriverWait(self._web_driver, timeout).until(
#                EC.presence_of_all_elements_located(self._locator)
#             )
#         except:
#             print(colored('Elements not found on the page!', 'red'))
#
#         return elements
#
#     def _set_value(self, web_driver, value):
#         """ Note: this action is not applicable for the list of elements. """
#         raise NotImplemented('This action is not applicable for the list of elements')
#
#     def click(self, hold_seconds=0, x_offset=0, y_offset=0):
#         """ Note: this action is not applicable for the list of elements. """
#         raise NotImplemented('This action is not applicable for the list of elements')
#
#     def count(self):
#         """ Get count of elements. """
#
#         elements = self.find()
#         return len(elements)
#
#     def get_text(self):
#         """ Get alert_text of elements. """
#
#         elements = self.find()
#         result = []
#
#         for element in elements:
#             text = ''
#
#             try:
#                 text = str(element.text)
#             except Exception as e:
#                 print('Error: {0}'.format(e))
#
#             result.append(text)
#
#         return result
#
#     def get_attribute(self, attr_name):
#         """ Get attribute of all elements. """
#
#         results = []
#         elements = self.find()
#
#         for element in elements:
#             results.append(element.get_attribute(attr_name))
#
#         return results
#
#     def highlight_and_make_screenshot(self, file_name='element.png'):
#         """ Highlight elements and make the screen-shot of all page. """
#
#         elements = self.find()
#
#         for element in elements:
#             # Scroll page to the element:
#             self._web_driver.execute_script("arguments[0].scrollIntoView();", element)
#
#             # Add red border to the style:
#             self._web_driver.execute_script("arguments[0].style.border='3px solid red'", element)
#
#         # Make screen-shot of the page:
#         self._web_driver.save_screenshot(file_name)
