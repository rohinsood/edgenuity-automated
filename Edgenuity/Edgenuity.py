from Utils import *
from .Handling import *

def activeSession():
    try:
        waitFindElementClick(By.NAME, 'continue')

        formatPrint("Becoming active session")

    except TimeoutException:

        pass

def closeAnnouncement():

    try:
        waitFindElementClick(By.XPATH, '//button[@class="close"]')
        formatPrint("Closing announcement")

    except TimeoutException:
        pass

def nextActivity():

    waitFindElementClick(By.XPATH, '//a[@title="Next Activity"]')
    
    formatPrint("Next activity", color=Fore.RED)


def completeActivity():

    driver.switch_to.default_content()

    try: 
        waitFindElementClick(By.XPATH, '//button[@href="#activity"]')
        formatPrint("Switching out of Enotes")

    except TimeoutException: ...

    activity_type = waitFindElement(By.XPATH, '//h2[@id="activity-title"]').text
    formatPrint(("Activity type: " + activity_type))
            
    if (activity_type == "Instruction" or activity_type == "Warm-Up" or activity_type == "Summary" or activity_type == "Assignment"):
       
        switchToStage()

        driver.execute_script('document.getElementById("invis-o-div").style.display = "none";')

        try:
            
            total_frames = waitFindElements(By.XPATH, '//ol[@class="FramesList"]/li')

        except StaleElementReferenceException:
            completeActivity()

        activity_frames = total_frames
        activity_frames.pop(0)
        activity_frames.pop( (len(activity_frames))-1 )

        switchToStage()

        for index, frame in enumerate(activity_frames):

            if ((frame.get_attribute("class") == "FrameCurrent")):
                upcoming_frames = list(dropwhile( lambda completedFrame: completedFrame != frame, activity_frames ))
                break

            elif ((frame.get_attribute("class") == "FrameCurrent FrameComplete")):
                formatPrint("Next Frame", color=Fore.RED)

                switchToStage()

                try:
                    waitFindElementClick(By.XPATH, '//li[@class="FrameRight"]/a')

                except TimeoutException:
                    activity_frames[index+1].click()

                continue

        next_check = False
        
        for frame in upcoming_frames:

            if(next_check):
                frame.click()
                next_check = False

            try:
                switchToPreview()
                waitFindElement(By.CLASS_NAME, 'title-bar')

                formatPrint("Question detected")

                if (activity_type == "Assignment"):

                    handleQuestion()
                
                else:
                    
                    switchToStage()

                    try:
                        done_button = waitFindElement(By.XPATH, '//span[@id="btnCheck"]')

                    except TimeoutException:
                        switchToPreview()

                        try:     
                            done_button_orange = waitFindElement(By.XPATH, '//div[@class="done-start"]', timeout=1)
                            done_button = []

                        except TimeoutException:
                            try:
                                done_button_orange = waitFindElement(By.XPATH, '//div[@class="done-retry"]', timeout=1)
                                done_button = []

                            except TimeoutException: 
                                break
                    
                    switchToStage()
                    
                    count = 0;

                    while True:
                        
                        switchToStage()

                        try: 

                            waitFindElement(By.XPATH, '//div[@id="invis-o-div"]', timeout=.5)

                        except TimeoutException:
                            
                            switchToPreview()
                            
                            try:
                                waitFindElementClick(By.XPATH, '//div[@class="answer-choice"]')

                            except ElementClickInterceptedException: continue

                            except TimeoutException: ...

                            if done_button == []:
                                done_button_orange.click()
                                count += 1

                            else:

                                try:
                                    switchToStage()
                                    done_button.click()
                                    count += 1

                                except ElementNotInteractableException:
                                    break
                                except StaleElementReferenceException:
                                    continue
                                except ElementClickInterceptedException:
                                    continue

                    switchToStage()
                    
                    waitForQuestionCompletion()

                    try: 
                        
                        try:
                            waitFindElementClick(By.XPATH, '//li[@class="FrameRight"]/a')
                        except ElementClickInterceptedException: ...

                        formatPrint("Next Frame", color=Fore.RED)

                        continue

                    except TimeoutException:

                        next_check = True
                        continue

                if (frame == upcoming_frames[( len(upcoming_frames)-1 )] and (frame.value_of_css_property("class") == "FrameCurrent FrameComplete")):
                    
                    break
                
            except TimeoutException:...

            switchToStage()
            
            try:
                waitForQuestionCompletion()

            except StaleElementReferenceException:
                break
            
            switchToStage()

            formatPrint("Next Frame", color=Fore.RED)

            try: 

                waitFindElementClick(By.XPATH, '//li[@class="FrameRight"]/a')

            except TimeoutException:

                next_check = True
                continue
    else:

        cont = formatInput("Continue? (y/n) ") 
        while cont != "y" and cont != "n":
            cont = formatInput("Continue? (y/n) ") 

        if (cont == 'y'):

            formatPrint("Continuing...")

            switchToStage()

            try:
                waitFindElementClick(By.XPATH, '//button[@data-bind="click: $root.startActivity"]')

            except TimeoutException: ...

            try: 
                waitFindElementClick(By.XPATH, '//a[@href="#activity"]')
                formatPrint("Switching out of Enotes")

            except TimeoutException: ...

            switchToStage()

            while True:

                goodluck_string = Fore.GREEN + "Good Luck!" + Fore.WHITE + " (n to go to the next activity when submitted) "
                goodluck_prompt = formatInput(goodluck_string)

                if (goodluck_prompt == 'n'):
                    break

                else:

                    try:
                        parent = waitFindElement(By.XPATH, '//div[@class="Assessment_Main_Body_Content_Question"][@style="display: block;"]/form/div/div[@class="Question_Contents"]/div')
                        multipleChoice(parent=parent)
                        
                    except TimeoutException:
                        try:
                            parent = waitFindElement(By.XPATH, '//div[@class="Assessment_Main_Body_Content_Question"][@style="display: block;"]/form/div/div[@class="Question_Contents"]')
                            dropdown(parent=parent)
                        except TimeoutException:
                            formatPrint("Unable to search", color=Fore.RESET)

    driver.switch_to.default_content()

    try:

        waitFindElementClick(By.XPATH, '//a[@class="footnav goRight"]')

        try:
            nextActivity()
        except TimeoutException: ...

    except TimeoutException:

        nextActivity()

    next_activity_string = "\n" + Fore.GREEN + "\e\> " + Fore.RED + "Next Activity"
    formatPrint(next_activity_string)

    completeActivity()

