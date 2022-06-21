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

ch_options=webdriver.ChromeOptions()
ch_options.add_experimental_option("detach", True)
# ch_options.add_argument("--headless")
ch_options.add_argument('log-level=3')
ch_options.add_argument('−−mute−audio')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=ch_options)

driver.get("https://launchpad.classlink.com/poway")

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
edgenuity_click.release()

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

# store frames
total_frames = waitFindElements(By.XPATH, '//ol[@class="FramesList"]/li')

# create activity frames
activity_frames = total_frames

# remove the last and first frames (nav btns)
activity_frames.pop(0)
activity_frames.pop( (len(activity_frames)-1) )

# find current frame
for frame in activity_frames:

    # remove elements before the current frame
    if ((frame.get_attribute("class") == "FrameCurrent")):
        upcoming_frames = list(dropwhile( lambda completedFrame: completedFrame != frame, total_frames ))
        break

    # go to next frame if the frame is marked as complete
    elif ((frame.get_attribute("class") == "FrameCurrent FrameComplete")):
        next_frame = waitFindElement(By.XPATH, '//li[@class="FrameRight"]/a')
        next_frame.click()
        continue

# iterate through all upcoming frames
for frame in upcoming_frames:

    # check if frame is a question or video
    try:

        # hover over the video element so that the play button and timings are visible
        video = waitFindElement(By.XPATH, '//video[@id="home_video_js"]')

        hover = ActionChains(driver=driver)
        hover.move_to_element(video)

        hover.perform()
        # click play if needed
        try:
            paused = waitFindElement(By.XPATH, '//li[@class="play"]')
            paused.click()

        except TimeoutException:
            pass

        # this is in "m:s / m:s" format, the fisrt m:s is the time passed, the second m:s is the video length 
        video_timer = (waitFindElement(By.XPATH, '//li[@id="uid1_time"]').text).split(" / ")
        time_passed_ms = video_timer[0]
        video_length_ms = video_timer[1]

        # convert to seconds
        video_length_ms = video_length_ms.split(":")
        video_length_s = (int(video_length_ms[0])*60) + int(video_length_ms[1])
        
        time_passed_ms = time_passed_ms.split(":")
        time_passed_s = (int(time_passed_ms[0])*60) + int(time_passed_ms[1])

        count = 0
        time_passed_log = []

        # wait for the video to finish
        while((time_passed_s != video_length_s)):

            # update time_passed every tick
            video_timer = waitFindElement(By.XPATH, '//li[@class="timer"]')
            
            video_timer = video_timer.text.split(" / ")
            time_passed_ms = (video_timer[0]).split(":")

            time_passed_s = (int(time_passed_ms[0])*60) + int(time_passed_ms[1])
            
            # sometimes the video ends 1 second early, so we check if time_passed_s is the same value 3 times in a row & if that value is 1 less than the video length
            count += 1
            time_passed_log.append(time_passed_s)

            if(count == 3):
                
                time_passed_check = (time_passed_log[0] == time_passed_log[2]) and (time_passed_log[0] == time_passed_log[1]) and (time_passed_log[1] == time_passed_log[2]) and ((time_passed_log[0]+1) == video_length_s)

                if(time_passed_check):
                    break
                
                # reset count & clear time_passed_log to every 3 iterations
                time_passed_log = []
                count = 0

        # click next frame or exit the loop when on the last frame
        if (frame == upcoming_frames[( len(upcoming_frames)-1 )]):
            break

        else: 
            next_frame = waitFindElement(By.XPATH, '//li[@class="FrameRight"]/a')
            next_frame.click()
            continue

    except TimeoutException:

        # alert the user that they are on a questions
        driver.execute_script("alert('You are on a question frame!');")
        
        # wait for alert to be dismissed
        while True:
            try:
                driver.switch_to.alert
            except:
                break
        
        # wait for frame to be completed
        current_or_complete = frame.get_attribute("class")
        while ((current_or_complete != "FrameCurrent  FrameComplete") or (current_or_complete == "FrameCurrent FrameComplete")): 
            current_or_complete = frame.get_attribute("class")
        
        # click next frame or exit the loop if on the last frame
        if (frame == upcoming_frames[( len(upcoming_frames)-1 )]):
            break

        else: 
            next_frame = waitFindElement(By.XPATH, '//li[@class="FrameRight"]/a')
            next_frame.click()
            continue

driver.quit()
print("Script completed successfully!")