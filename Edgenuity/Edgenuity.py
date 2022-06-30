from Utils import *

def activeSession():
    try:
        active_sesh = waitFindElement(By.NAME, 'continue')
        active_sesh.click()

        print("Becoming active session")

    except TimeoutException:

        pass

def nextActivity():

    next_activity = waitFindElement(By.XPATH, '//a[@title="Next Activity"]')
    next_activity.click()

    print(Fore.RED + "~ Next activity ~" + Fore.RESET)

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

            upcoming_frames = list(dropwhile( lambda completedFrame: completedFrame != frame, activity_frames ))
            break

        elif ((frame.get_attribute("class") == "FrameCurrent FrameComplete")):
            
            print(Fore.RED + "~ Next Frame ~" + Fore.RESET)

            waitFindElementClick(By.XPATH, '//li[@class="FrameRight"]/a')
            continue
    
    for frame in upcoming_frames:
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
            
        except TimeoutException:

            print(Fore.MAGENTA + "Video Detected" + Fore.RESET)

        driver.switch_to.default_content()
        driver.switch_to.frame(stage_iframe)

        if (frame == upcoming_frames[( len(upcoming_frames)-1 )] and (frame.value_of_css_property("class") == "FrameCurrent FrameComplete")):
                
            print(Fore.RED + "~ Last frame ~" + Fore.RESET)
            break
        
        driver.switch_to.default_content()
        driver.switch_to.frame(stage_iframe)

        try:
            waitForOpacityChange(By.XPATH, '//li[@class="FrameRight"]')
        except StaleElementReferenceException:
            break

        print(Fore.RED + "~ Next frame ~" + Fore.RESET)
        waitFindElementClick(By.XPATH, '//li[@class="FrameRight"]/a')
        continue

            
    print(Fore.LIGHTMAGENTA_EX + "~ Activity successfully completed! ~" + Fore.RESET)

    driver.quit()

def handleQuestion():
    question_container = waitFindElement(By.XPATH, '//div[@fstack]')

    search_strings = []
    try:
        
        try:

            reading = waitFindElement(By.XPATH, '//div[@class="reading pane-blue"]', parent=question_container).text
            print(Fore.LIGHTCYAN_EX + "    Reading MC question detected" + Fore.RESET)

            search_strings.append('"' + reading + '"')

        except TimeoutException:

            print(Fore.CYAN + "  Multiple choice question detected" + Fore.RESET)

        question_content = waitFindElements(By.XPATH, '//div[@class="Practice_Question_Body"]', parent=question_container)
        question = question_content[0].text

        search_strings.append('"' + question + '"')
        
        answer_choices = waitFindElements(By.XPATH, '//div[@class="answer-choice"]', parent=question_content[1])
        answer_choices = [choice.text for choice in answer_choices]

        [search_strings.append('"' + choice + '"') for choice in answer_choices]

        search_string = ' '.join(search_strings)

        driver.switch_to.new_window('tab')
        driver.get('https://www.google.com/search?q=' + search_string)
        driver.switch_to.window(driver.window_handles[0])

    except TimeoutException:
        
        try:
            search_strings = []

            dropdown_question = waitFindElements(By.XPATH, '//form/p', parent=question_container)

            dropdown_question = [choice.text for choice in dropdown_question]
            [search_strings.append('"' + choice + '"') for choice in dropdown_question]
            
            print(Fore.CYAN + "    Dropdown MC detected" + Fore.RESET)

            search_string = ' '.join(search_strings)

            driver.switch_to.new_window('tab')
            driver.get('https://www.google.com/search?q=' + search_string)
            driver.switch_to.window(driver.window_handles[0])

        except TimeoutException:

            waitFindElement('//div[@id="matchingActivity"]')
            print(Fore.CYAN + "    Matching activity detected" + Fore.RESET)  