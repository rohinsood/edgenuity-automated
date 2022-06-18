from distutils.command.build import build
from itertools import dropwhile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

ch_options=webdriver.ChromeOptions()
ch_options.add_experimental_option("detach", True)
ch_options.add_argument('log-level=3')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=ch_options)

driver.get("https://launchpad.classlink.com/poway")

wait = WebDriverWait(driver=driver, timeout=10)

def findElement( finder: By, element: str ):
    return driver.find_element(finder, element)
    
def findElements( finder: By, element: str ):
    return driver.find_elements(finder, element)    

def waitFindElement( finder: By, element: str):
    wait.until(EC.element_to_be_clickable(
            (finder, element)
        )
    )
    
    return driver.find_element(finder, element)

def waitFindElements( finder: By, element: str):
    wait.until(EC.element_to_be_clickable(
            (finder, element)
        )
    )
    
    return driver.find_elements(finder, element)

