from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

path = r"C:\Users\HP\PycharmProjects\python_selenium_project\Drivers\chromedriver.exe"
options = Options()
options.add_experimental_option('detach', True)
service = Service(executable_path=path)

driver = webdriver.Chrome(options=options)


class _visibility_of_the_element_located(visibility_of_element_located):
    def __call__(self, driver):
        displayed = super().__call__(driver)
        if isinstance(displayed, WebElement):
            return displayed.is_enabled()
        else:
            return False


wait = WebDriverWait(driver, timeout=10)
wait.until(_visibility_of_the_element_located("name", "fname"))
driver.find_elements("xpath", "value")


################################################################################################################

# using the decorator an alternate solution

def _is_visible_enabled(locator):  # here locator is locator type and locator value
    def wrapper(driver):
        try:
            displayed = driver.find_elements(*locator).is_displayed()
            enabled = driver.find_elements(*locator).is_enabled()
        except(BaseException):
            return False
        return displayed and enabled

    return wrapper

wait = WebDriverWait(driver, timeout=10)
wait.until(_is_visible_enabled("name", "fname"))