import time
from locators.main_page_locators import MainPageLocators
from pages._base import WebPage
from pages._elements import WebElement


class MainPage(WebPage):
    elements_menu = WebElement(*MainPageLocators.ELEMENTS_MENU)
