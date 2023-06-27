from selenium.webdriver.common.by import By


class TextBoxPageLocators:
    #  Input fields
    FULL_NAME_INPUT = (By.CSS_SELECTOR, 'input[id="userName"]')
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[id="userEmail"]')
    CURRENT_ADDRESS_INPUT = (By.CSS_SELECTOR, 'textarea[id="currentAddress"]')
    PERMANENT_ADDRESS_INPUT = (By.CSS_SELECTOR, 'textarea[id="permanentAddress"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[id="submit"]')

    #  Output fields
    FULL_NAME_OUTPUT = (By.CSS_SELECTOR, '#output #name')
    EMAIL_OUTPUT = (By.CSS_SELECTOR, '#output #email')
    CURRENT_ADDRESS_OUTPUT = (By.CSS_SELECTOR, '#output #currentAddress')
    PERMANENT_ADDRESS_OUTPUT = (By.CSS_SELECTOR, '#output #permanentAddress')

