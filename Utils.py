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
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException

chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--window-size=980,1080")
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('−−mute−audio')
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

wait = WebDriverWait(driver=driver, timeout=5)

def findElement( finder: By, element: str, implicit_wait=0 ):
    driver.implicitly_wait(implicit_wait)

    return driver.find_element(finder, element)
    
def findElements( finder: By, element: str, implicit_wait=0 ):
    driver.implicitly_wait(implicit_wait)

    return driver.find_elements(finder, element)    

def waitFindElement( finder: By, element: str ):
    wait.until(EC.element_to_be_clickable(
            (finder, element)
        )
    )

    return driver.find_element(finder, element)

def waitFindElements( finder: By, element: str ):
    wait.until(EC.element_to_be_clickable(
            (finder, element)
        )
    )

    return driver.find_elements(finder, element)

def waitFindElementClick ( finder: By, element: str):
    wait.until(EC.element_to_be_clickable(
            (finder, element)
        )
    )

    driver.find_element(finder, element).click()

def waitForOpacityChange ( finder: By, element: str ):
    opacity_element = waitFindElement(finder, element)
    
    print("Waiting for next button to flash")

    # wait for opacity to change
    while ((opacity_element.get_attribute('style') == "") or (opacity_element.get_attribute('style') == "opacity: 1;")):
        try:
            opacity_element = waitFindElement(finder, element)
        except NoSuchElementException:
            break

    opacity_element = waitFindElement(finder, (element + "/a"))
    opacity_element.click()

    

    