from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains


driver = Chrome("C:\Users\HP\PycharmProjects\python_selenium_project\Drivers\chromedriver.exe")
driver.maximize_window()
# setting implicitly wait to 3 sec which acts for entire browser session
driver.implicitly_wait(3)
driver.get(r"https://twitter.com/home")

driver.find_element("xpath", "//span[text()='Next']").click()



'''
class Twitter:
    
    
    def __int__(self, username):
        self.driver = Chrome("C:\Users\HP\PycharmProjects\python_selenium_project\Drivers\chromedriver.exe")
        self.driver.maximize_window()
        sleep(2)
        self.driver.get(r"https://twitter.com/home")
        sleep(2)
        self.driver.find_element("name", "text").click()
        sleep()
        self.driver.find_element("name", "text").send_keys(username)
        sleep(2)
        self.driver.find_element("xpath", "//span[text()='Next']").click()
        sleep(2)


username = "abcd"
Twitter(username)
'''