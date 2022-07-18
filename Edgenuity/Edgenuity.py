from Utils import *
from .Handling import *

def activeSession():
    try:
        waitFindElementClick(By.NAME, 'continue')

        print("Becoming active session")

    except TimeoutException:

        pass

def closeAnnouncement():
    try:
        waitFindElementClick(By.XPATH, '//button[@class="close"]')
        print("Closing announcement")

    except TimeoutException:
        pass

def nextActivity():

    waitFindElementClick(By.XPATH, '//a[@title="Next Activity"]')

    print(Fore.GREEN + "~ Next activity ~" + Fore.RESET)


def completeActivity():

    try: 
        waitFindElementClick(By.XPATH, '//button[@href="#activity"]')
        print("Switching out of Enotes")

    except TimeoutException: ...

    activity_type = waitFindElement(By.XPATH, '//h2[@id="activity-title"]').text
    print(Fore.GREEN + "~ Activity type: " + activity_type + Fore.RESET)
            
    if (activity_type == "Instruction" or activity_type == "Warm-Up" or activity_type == "Summary"):
        try:
            switchToStage()
            
            total_frames = waitFindElements(By.XPATH, '//ol[@class="FramesList"]/li')
            print("Finding frames on assignment")

        except StaleElementReferenceException:

            completeActivity()

        activity_frames = total_frames
        activity_frames.pop(0)
        activity_frames.pop( (len(activity_frames))-1 )
        print("Setting up frame storage")

        for frame in activity_frames:

            if ((frame.get_attribute("class") == "FrameCurrent")):

                upcoming_frames = list(dropwhile( lambda completedFrame: completedFrame != frame, activity_frames ))
                break

            elif ((frame.get_attribute("class") == "FrameCurrent FrameComplete")):
                
                print(Fore.RED + "~ Next Frame ~" + Fore.RESET)

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

                print(Fore.GREEN + "Question detected" + Fore.RESET)

                try:

                    intro_audio = waitFindElement(By.XPATH, '//span[@id="btnEntryAudio"]')
                    while(intro_audio.value_of_css_property("display") == "None"):
                        intro_audio = waitFindElement(By.XPATH, '//span[@id="btnEntryAudio"]')

                except TimeoutException:
                    pass
                
                handleQuestion()

                if (frame == upcoming_frames[( len(upcoming_frames)-1 )] and (frame.value_of_css_property("class") == "FrameCurrent FrameComplete")):
                    
                    print(Fore.RED + "~ Last frame ~" + Fore.RESET)
                    break
                
            except TimeoutException:...

            switchToStage()
            
            try:
                waitForOpacityChange(By.XPATH, '//li[@class="FrameRight"]')

            except StaleElementReferenceException:
                break
            
            switchToStage()

            print(Fore.RED + "~ Next frame ~" + Fore.RESET)
            try: 

                waitFindElementClick(By.XPATH, '//li[@class="FrameRight"]/a')

            except TimeoutException:

                next_check = True
                continue

    else:

        cont = input("  Continue? (y/n) ") 
        while cont != "y" and cont != "n":
            cont = input("  Continue? (y/n) ") 

        if (cont == 'y'):

            print("  Continuing...")

            try:
                waitFindElementClick(By.XPATH, '//button[@data-bind="click: $root.startActivity"]')

            except TimeoutException: ...

            try: 
                waitFindElementClick(By.XPATH, '//a[@href="#activity"]')
                print("Switching out of Enotes")

            except TimeoutException: ...

            switchToStage()

            runThread()

    driver.switch_to.default_content()

    try:

        waitFindElementClick(By.XPATH, '//a[@class="footnav goRight"]')

    except TimeoutException:

        nextActivity()

    print(Fore.GREEN + "~ Next activity ~" + Fore.RESET)
    
    completeActivity()

