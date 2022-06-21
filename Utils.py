from itertools import dropwhile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--window-size=840,640")
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('−−mute−audio')
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

wait = WebDriverWait(driver=driver, timeout=5)

def findElement( finder: By, element: str ):
    return driver.find_element(finder, element)
    
def findElements( finder: By, element: str ):
    return driver.find_elements(finder, element)    

def waitFindElement( finder: By, element: str, implicit_wait=0):
    wait.until(EC.element_to_be_clickable(
            (finder, element)
        )
    )
    
    driver.implicitly_wait(implicit_wait)

    return driver.find_element(finder, element)

def waitFindElements( finder: By, element: str, implicit_wait=0 ):
    wait.until(EC.element_to_be_clickable(
            (finder, element)
        )
    )
    
    driver.implicitly_wait(implicit_wait)

    return driver.find_elements(finder, element)