from itertools import dropwhile
import time
from selenium import webdriver
from colorama import Fore, Back, Style
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
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from threading import Thread

chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--window-size=980,1080")
chrome_options.add_argument('log-level=3')
chrome_options.add_argument('−−mute−audio')
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

wait = WebDriverWait(driver=driver, timeout=1.5)

def formatPrint( string: str, color=Fore.WHITE, recursive=False ):
    terminal_format = Fore.GREEN + r"\e\> " 
    print(terminal_format + color + string + Fore.RESET, end="\r") if recursive else print(terminal_format + color + string)

def formatInput( string: str, color=Fore.WHITE ):
    terminal_format = Fore.GREEN + r"\e\> " 
    return input(terminal_format + color + string + Fore.RESET)

def findElement( finder: By, element: str, implicit_wait=0, parent=None ):
    driver.implicitly_wait(implicit_wait)

    if parent is None:
        return driver.find_element(finder, element)
    else:
        return parent.find_element(finder, element)
    
def findElements( finder: By, element: str, implicit_wait=0, parent=None ):
    driver.implicitly_wait(implicit_wait)

    if parent is None:
        return driver.find_elements(finder, element)
    else:
        return parent.find_elements(finder, element)   


def waitFindElement ( finder: By, element: str, parent=None, timeout=0 ):

    if (timeout != 0):
        wait = WebDriverWait(driver=driver, timeout=timeout)
        wait.until(EC.element_to_be_clickable(
                (finder, element)
            )
        )
    else:
        wait = WebDriverWait(driver=driver, timeout=2)
        wait.until(EC.element_to_be_clickable(
                (finder, element)
            )
        )

    if parent is None:
        return driver.find_element(finder, element)
    else:
        return parent.find_element(finder, element)


def waitFindElements( finder: By, element: str, parent=None, timeout=0 ):
    if (timeout != 0):
        wait = WebDriverWait(driver=driver, timeout=timeout)
        wait.until(EC.element_to_be_clickable(
                (finder, element)
            )
        )
    else:
        wait = WebDriverWait(driver=driver, timeout=2)
        wait.until(EC.element_to_be_clickable(
                (finder, element)
            )
        )

    if parent is None:
        return driver.find_elements(finder, element)
    else:
        return parent.find_elements(finder, element)

def findElementClick ( finder: By, element: str, implicit_wait=0 ):

    driver.implicitly_wait(implicit_wait)
    driver.find_element(finder, element).click()

def waitFindElementClick ( finder: By, element: str):
    wait.until(EC.element_to_be_clickable(
            (finder, element)
        )
    )

    driver.find_element(finder, element).click()

def waitForQuestionCompletion ():
    opacity_element = waitFindElement(By.XPATH, '//li[@class="FrameRight"]')
    
    start_time = time.time()
    while ((opacity_element.get_attribute('style') == "") or (opacity_element.get_attribute('style') == "opacity: 1;")):
        end_time = time.time()
        time_lapsed = str(round((end_time - start_time), 1))
        update_string = Fore.YELLOW + "Waiting for frame to be marked as complete " + Fore.WHITE  + " < Time lapsed: " + time_lapsed + " >" + Fore.RESET
        formatPrint( update_string, recursive="\r", )

        try:
            opacity_element = findElement(By.XPATH, '//li[@class="FrameRight"]')
        except NoSuchElementException:
            break
    
    print("")
