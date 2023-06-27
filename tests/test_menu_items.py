import time
from pages.main_page import MainPage


class TestMenuItems:
    def test_elements_menu(self, web_browser):
        main_page = MainPage(web_browser)
        main_page.elements_menu.find()
        main_page.elements_menu.click()
        time.sleep(5)
