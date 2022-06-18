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

# login to myplan
username_input = waitFindElement(By.ID, "username")
username_input.send_keys("1861253")

password_input = waitFindElement(By.ID, "password")
password_input.send_keys("FlatwoundChamba1028$")

password_input.send_keys(Keys.RETURN)

# open edgenuity through app link
edgenuity_link = waitFindElement(By.XPATH, '//application[@aria-label="Edgenuity (Student)"]')

edgenuity_click = ActionChains(driver=driver)
edgenuity_click.context_click(edgenuity_link).send_keys(Keys.RETURN)
edgenuity_click.perform()

# close myplan
driver.switch_to.window(driver.window_handles[0])
driver.close()
driver.switch_to.window(driver.window_handles[0])

# become the current active session if necessary
try:
    active_sesh = waitFindElement(By.NAME, 'continue')
    active_sesh.click()
except:
    pass

# next activity
next_activity = waitFindElement(By.XPATH, '//a[@title="Next Activity"]')
next_activity.click()

# switch to iFrame element 
iFrame = waitFindElement(By.XPATH, "//iframe")
driver.switch_to.frame(iFrame)

# store frames
total_frames = waitFindElements(By.XPATH, '//ol[@class="FramesList"]/li')

# store the next btn
next_frame = total_frames[ (len(total_frames)-1) ]

# remove the last and first frames (nav btns)
total_frames.pop(0)
total_frames.pop( (len(total_frames)-1) )

# store the next btn
next_frame = total_frames[ (len(total_frames)-1) ]

# remove the last and first frames (nav btns)
total_frames.pop(0)
total_frames.pop( (len(total_frames)-1) )

# find current frame
for frame in total_frames:

    # remove elements before the current frame
    if (frame.get_attribute("class") == "FrameCurrent"):
        upcoming_frames = list(dropwhile( lambda completedFrame: completedFrame != frame, total_frames ))
        break
    else:
        continue
