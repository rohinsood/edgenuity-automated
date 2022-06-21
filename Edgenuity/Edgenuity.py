from Utils import *

def activeSession():
    try:
        active_sesh = waitFindElement(By.NAME, 'continue')
        active_sesh.click()
    except TimeoutException:
        pass

def nextActivity():
    next_activity = waitFindElement(By.XPATH, '//a[@title="Next Activity"]')
    next_activity.click()

def switchToIframe():
    iFrame = waitFindElement(By.XPATH, "//iframe")
    driver.switch_to.frame(iFrame)

def completeActivity():
    total_frames = waitFindElements(By.XPATH, '//ol[@class="FramesList"]/li')
    activity_frames = total_frames
    activity_frames.pop(0)
    activity_frames.pop( (len(activity_frames)-1) )
    for frame in activity_frames:

        if ((frame.get_attribute("class") == "FrameCurrent")):

            upcoming_frames = list(dropwhile( lambda completedFrame: completedFrame != frame, total_frames ))
            break
        elif ((frame.get_attribute("class") == "FrameCurrent FrameComplete")):

            next_frame = waitFindElement(By.XPATH, '//li[@class="FrameRight"]/a')
            next_frame.click()
            continue
    
    for frame in upcoming_frames:
        try:

            video = waitFindElement(By.XPATH, '//video[@id="home_video_js"]')

            hover = ActionChains(driver=driver)
            hover.move_to_element(video)

            hover.perform()
            try:
                paused = waitFindElement(By.XPATH, '//li[@class="play"]')
                paused.click()

            except TimeoutException:
                pass

            video_timer = (waitFindElement(By.XPATH, '//li[@id="uid1_time"]').text).split(" / ")
            time_passed_ms = video_timer[0]
            video_length_ms = video_timer[1]

            video_length_ms = video_length_ms.split(":")
            video_length_s = (int(video_length_ms[0])*60) + int(video_length_ms[1])
            
            time_passed_ms = time_passed_ms.split(":")
            time_passed_s = (int(time_passed_ms[0])*60) + int(time_passed_ms[1])

            count = 0
            time_passed_log = []

            while((time_passed_s != video_length_s)):

                video_timer = waitFindElement(By.XPATH, '//li[@class="timer"]')
                
                video_timer = video_timer.text.split(" / ")
                time_passed_ms = (video_timer[0]).split(":")

                time_passed_s = (int(time_passed_ms[0])*60) + int(time_passed_ms[1])
                
                count += 1
                time_passed_log.append(time_passed_s)

                if(count == 3):
                    
                    time_passed_check = (time_passed_log[0] == time_passed_log[2]) and (time_passed_log[0] == time_passed_log[1]) and (time_passed_log[1] == time_passed_log[2]) and ((time_passed_log[0]+1) == video_length_s)

                    if(time_passed_check):
                        break
                    
                    time_passed_log = []
                    count = 0

            if (frame == upcoming_frames[( len(upcoming_frames)-1 )]):
                break

            else: 
                next_frame = waitFindElement(By.XPATH, '//li[@class="FrameRight"]/a')
                next_frame.click()
                continue

        except TimeoutException:

            driver.execute_script("alert('You are on a question frame!');")
            
            while True:
                try:
                    driver.switch_to.alert
                except:
                    break
            
            current_or_complete = frame.get_attribute("class")
            while ((current_or_complete != "FrameCurrent  FrameComplete") or (current_or_complete == "FrameCurrent FrameComplete")): 
                current_or_complete = frame.get_attribute("class")
            
            if (frame == upcoming_frames[( len(upcoming_frames)-1 )]):
                break

            else: 
                next_frame = waitFindElement(By.XPATH, '//li[@class="FrameRight"]/a')
                next_frame.click()
                continue