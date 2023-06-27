import os
import pytest
from selenium import webdriver


# def pytest_addoption(parser):
#     parser.addoption('--env', action='store', default=None, help="Select env")


@pytest.fixture(scope='class')
def web_browser(request):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--log-level=DEBUG')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # chrome_options.add_argument('--headless')

    prefs = {'download.default_directory': (os.getcwd() + r'\test_data').replace('/', '\''),
             'download.prompt_for_download': False,
             'download.directory_upgrade': True,
             'safebrowsing.enabled': False,
             }
    chrome_options.add_experimental_option("prefs", prefs)

    # # Define environment
    # env = request.config.getoption("env")  # get environment
    # link = None
    # if env == 'dev':
    #     link = 'https://portal.dev.com/'
    # elif env == 'qa':
    #     link = 'https://portal.qa.com/'
    # elif env == 'staging':
    #     link = 'https://portal.staging.com/'
    # elif env == 'production':
    #     link = 'https://portal.prod.com/'

    browser = webdriver.Chrome(options=chrome_options)
    link = 'https://demoqa.com/'
    browser.get(link)

    yield browser
    browser.close()
    browser.quit()
