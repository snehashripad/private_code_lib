import subprocess
from time import sleep

import undetected_chromedriver as webdriver


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--use_subprocess")
# subprocess.Popen( args=[exec_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)

driver = webdriver.Chrome(options=chrome_options)

driver.get(rf"https://www.epw.in/")
sleep(5)

driver.save_screenshot("screenshot.png")

