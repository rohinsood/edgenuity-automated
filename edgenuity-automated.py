from distutils.command.build import build
from itertools import dropwhile
from socket import timeout
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time as real_time
from selenium.common.exceptions import TimeoutException

ch_options=webdriver.ChromeOptions()
ch_options.add_experimental_option("detach", True)
ch_options.add_argument('log-level=3')
ch_options.add_argument('−−mute−audio')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=ch_options)

driver.get("https://launchpad.classlink.com/poway")

wait = WebDriverWait(driver=driver, timeout=5)

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
except TimeoutException:
    pass

# next activity
next_activity = waitFindElement(By.XPATH, '//a[@title="Next Activity"]')
next_activity.click()

# switch to iFrame element 
iFrame = waitFindElement(By.XPATH, "//iframe")
driver.switch_to.frame(iFrame)

# find next activity btn


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

# iterate through all upcoming frames
for index in range(len(upcoming_frames)):

    # check if frame is a question or video
    try:
        # this is in m:s / m:s format, the second m:s is the video length
        video_timer = waitFindElement(By.XPATH, '//li[@id="uid1_time"]').text

        # this isolates the second m:s into one string
        video_length_ms = (video_timer.split())[2]

        # this splits isoltes the minutes and seconds of the above strings & converts minutes to seconds to find the video length in seconds
        video_length_ms = video_length_ms.split(":")
        video_length_s = (int(video_length_ms[0])*60) + int(video_length_ms[1])

        # this waits for the video length
        real_time.sleep(video_length_s)

        # if the current frame is the last frame, click the next activity button and not the next frame button
        if (index == len(upcoming_frames)):
            # go to the next activity
            next_activity = waitFindElement()
            next_activity.click

        else: 
            # go to the next frame
            next_frame.click

    except TimeoutException:
        pass