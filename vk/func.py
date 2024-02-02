from selenium import webdriver


class Preconditions:
    def __init__(self):
        self.base_url = "https://vk.com/"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--allow-profiles-outside-user-dir')
        self.options.add_argument('--enable-profile-shortcut-manager')
        self.options.add_argument('user-data-dir=D:/Study/Python/selenium/ChromeUsers')
        self.options.add_argument('--profile-directory=VKBot')
        self.options.add_argument("--start-maximized")
        self.browser = webdriver.Chrome(self.options)
        self.browser.implicitly_wait(5)

    def start_browser(self):
        self.browser.get(self.base_url)


class BaseFunc:
    def __init__(self, browser):
        self.browser = browser

    def get_element(self, by, locator):
        return self.browser.find_element(by, locator)

    def get_elements(self, by, locator):
        return self.browser.find_elements(by, locator)

    def click_element(self, locator):
        self.get_element(*locator).click()

    def input_text(self, locator, text):
        element = self.get_element(*locator)
        element.clear()
        element.send_keys(text)
