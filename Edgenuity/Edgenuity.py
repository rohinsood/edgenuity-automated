from Utils import *

def login():

    lines = []
    with open("login.txt") as f:
        lines = f.readlines()

    USERNAME = lines[0].strip()
    PASSWORD = lines[1].strip() 

    print("Logging in...")
    driver.get("https://auth.edgenuity.com/Login/Login/Student")
    waitFindElement(By.ID, "LoginUsername").send_keys(USERNAME)
    waitFindElement(By.XPATH, '//input[@id="LoginPassword"]').send_keys(PASSWORD)
    waitFindElement(By.XPATH, '//button[@id="LoginSubmit"]').click()
    print("Logged in!")

def activeSession():
    try:
        active_sesh = waitFindElement(By.NAME, 'continue')
        active_sesh.click()

        print("--\(˙<>˙)/-- Becoming active session")

    except TimeoutException:

        pass

def nextActivity():

    next_activity = waitFindElement(By.XPATH, '//a[@title="Next Activity"]')
    next_activity.click()

    print("Going to the next activity")

def completeActivity():
    print("Switching to iframe")
    stage_iframe = waitFindElement(By.XPATH, '//iframe[@id="stageFrame"]')
    driver.switch_to.frame(stage_iframe)

    total_frames = waitFindElements(By.XPATH, '//ol[@class="FramesList"]/li')
    activity_frames = total_frames
    activity_frames.pop(0)
    activity_frames.pop( (len(activity_frames)-1) )

    print("Setting up frame storage")

    for frame in activity_frames:

        if ((frame.get_attribute("class") == "FrameCurrent")):

            print("Finding current frame")

            upcoming_frames = list(dropwhile( lambda completedFrame: completedFrame != frame, activity_frames ))
            break
        elif ((frame.get_attribute("class") == "FrameCurrent FrameComplete")):
            
            print("Current frame is already complete")

            next_frame = waitFindElement(By.XPATH, '//li[@class="FrameRight"]/a')
            next_frame.click()
            continue
    
    for frame in upcoming_frames:
        try:
            
            print("--\(˙<>˙)/-- Checking for question")

            video_iframe = waitFindElement(By.XPATH, '//iframe[@id="iFramePreview"]')
            driver.switch_to.frame(video_iframe)
            waitFindElement(By.CLASS_NAME, 'title-bar')

            print("Question Detected!")

            driver.switch_to.default_content()
            driver.switch_to.frame(stage_iframe)

            driver.execute_script("alert('You are on a question frame!');")
            
            print("Alerted!")
            
            while True:
                try:
                    driver.switch_to.alert
                except:
                    break
            
            waitForOpacityChange(By.XPATH, '//li[@class="FrameRight"]')
            
            print("Question complete!")

            if (frame == upcoming_frames[( len(upcoming_frames)-1 )]):
                
                print("Last frame!")
                break

            else: 

                print("Next frame!")
                continue
    

        except TimeoutException:

            print("Video Detected!")

            driver.switch_to.default_content()
            driver.switch_to.frame(stage_iframe)

            waitForOpacityChange(By.XPATH, '//li[@class="FrameRight"]')

            print("Video finished!")

            if (frame == upcoming_frames[( len(upcoming_frames)-1 )]):
                
                print("Last frame!")
                break

            else: 
                
                print("Next frame!")
                continue

            
    print("--\(˙<>˙)/-- Activity successfully completed!")

    driver.quit()