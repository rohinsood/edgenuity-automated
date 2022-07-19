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

    try: 
        waitFindElementClick(By.XPATH, '//button[@href="#activity"]')
        formatPrint("Switching out of Enotes")

    except TimeoutException: ...

    driver.switch_to.default_content()

    activity_type = waitFindElement(By.XPATH, '//h2[@id="activity-title"]').text
    formatPrint(("Activity type: " + activity_type), color=Fore.CYAN)
            
    if (activity_type == "Instruction" or activity_type == "Warm-Up" or activity_type == "Summary" or activity_type == "Assignment"):
        try:
            switchToStage()
            
            total_frames = waitFindElements(By.XPATH, '//ol[@class="FramesList"]/li')
            formatPrint("Finding frames on assignment")

        except StaleElementReferenceException:

            completeActivity()

        activity_frames = total_frames
        activity_frames.pop(0)
        activity_frames.pop( (len(activity_frames))-1 )
        formatPrint("Setting up frame storage")

        for frame in activity_frames:

            if ((frame.get_attribute("class") == "FrameCurrent")):

                upcoming_frames = list(dropwhile( lambda completedFrame: completedFrame != frame, activity_frames ))
                break

            elif ((frame.get_attribute("class") == "FrameCurrent FrameComplete")):
                
                formatPrint("Next Frame", color=Fore.RED)

                switchToStage()
                waitFindElementClick(By.XPATH, '//li[@class="FrameRight"]/a')
                continue

        next_check = False
        
        for frame in upcoming_frames:

            if(next_check):
                frame.click()
                next_check = False

            try:
                
                question_iframe = waitFindElement(By.XPATH, '//iframe[@id="iFramePreview"]')
                driver.switch_to.frame(question_iframe)
                waitFindElement(By.CLASS_NAME, 'title-bar')

                formatPrint("Question detected")

                try:

                    intro_audio = waitFindElement(By.XPATH, '//span[@id="btnEntryAudio"]')
                    while(intro_audio.value_of_css_property("display") == "None"):
                        intro_audio = waitFindElement(By.XPATH, '//span[@id="btnEntryAudio"]')

                except TimeoutException:
                    pass
                
                handleQuestion()
                    
                if (frame == upcoming_frames[( len(upcoming_frames)-1 )] and (frame.value_of_css_property("class") == "FrameCurrent FrameComplete")):
                    
                    break
                
            except TimeoutException:...

            switchToStage()
            
            try:
                waitForOpacityChange()

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

        while True:

            goodluck_string = Fore.GREEN + "Good Luck!" + Fore.WHITE + "(n to go to the next activity when done) "
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
                        print("Unable to search")

    driver.switch_to.default_content()

    try:

        waitFindElementClick(By.XPATH, '//a[@class="footnav goRight"]')

    except TimeoutException:

        nextActivity()

    formatPrint("Next activity", color=Fore.RED)

    completeActivity()

