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
    stage_iframe = waitFindElement(By.XPATH, '//iframe[@id="stageFrame"]', parent=None, timeout=10)
    driver.switch_to.frame(stage_iframe)

    try:
        total_frames = waitFindElements(By.XPATH, '//ol[@class="FramesList"]/li')
        activity_frames = total_frames
        activity_frames.pop(0)
        activity_frames.pop( (len(activity_frames))-1 )
        print("Setting up frame storage")

    except TimeoutException:

        activity_frames = []
        
        print(Fore.CYAN + "Test/Quiz Detected" + Fore.RESET)
        cont = input("  Continue? (y/n) ") 
        
        if (cont == 'y'):
            print("  Continuing...")


            waitFindElementClick(By.XPATH, '//button[@data-bind="click: $root.startActivity"]')

            questions = waitFindElements(By.XPATH, '//ol[@id="navBtnList"]/li', parent=None, timeout=10)
            questions.pop(0)

            print(questions)

            for question in questions:
                waitFindElementClick(By.XPATH, '//a[@id="nextQuestion"]')

                handleQuestion()
            
            questions[0].click()

    if (activity_frames != 0):
        for frame in activity_frames:

            if ((frame.get_attribute("class") == "FrameCurrent")):

                upcoming_frames = list(dropwhile( lambda completedFrame: completedFrame != frame, activity_frames ))
                break

            elif ((frame.get_attribute("class") == "FrameCurrent FrameComplete")):
                
                print(Fore.RED + "~ Next Frame ~" + Fore.RESET)

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
                
            except TimeoutException:

                print(Fore.MAGENTA + "Video Detected" + Fore.RESET)

            driver.switch_to.default_content()
            stage_iframe = waitFindElement(By.XPATH, '//iframe[@id="stageFrame"]')
            driver.switch_to.frame(stage_iframe)

            if (frame == upcoming_frames[( len(upcoming_frames)-1 )] and (frame.value_of_css_property("class") == "FrameCurrent FrameComplete")):
                    
                print(Fore.RED + "~ Last frame ~" + Fore.RESET)
                break
            
            try:
                waitForOpacityChange(By.XPATH, '//li[@class="FrameRight"]')
            except StaleElementReferenceException:
                break
            
            driver.switch_to.default_content()
            stage_iframe = waitFindElement(By.XPATH, '//iframe[@id="stageFrame"]')
            driver.switch_to.frame(stage_iframe)

            print(Fore.RED + "~ Next frame ~" + Fore.RESET)
            try: 
                waitFindElementClick(By.XPATH, '//li[@class="FrameRight"]/a')
            except TimeoutException:
                next_check = True
                continue
            
    print(Fore.LIGHTMAGENTA_EX + "~ Task successfully completed! ~" + Fore.RESET)

    driver.switch_to.default_content()
    waitFindElementClick(By.XPATH, '//a[@class="footnav goRight"]')

    completeActivity()

    print(Fore.RED + "~ Next activity ~" + Fore.RESET)


def handleQuestion():
    question_container = waitFindElement(By.XPATH, '//div[@fstack]')

    search_strings = []
    try:
        
        try:

            reading = waitFindElement(By.XPATH, '//div[@class="reading pane-blue"]', parent=question_container).text
            print(Fore.LIGHTCYAN_EX + "    Reading MC question detected" + Fore.RESET)

            search_strings.append('"' + reading + '"')

        except TimeoutException:
            pass

        question_content = waitFindElements(By.XPATH, '//div[@class="Practice_Question_Body"]', parent=question_container)
        question = question_content[0].text


        search_strings.append('"' + question + '"')
        
        answer_choices = waitFindElements(By.XPATH, '//div[@class="answer-choice"]', parent=question_content[1])
        answer_choices = [choice.text for choice in answer_choices]

        print(Fore.CYAN + "    Multiple choice question detected" + Fore.RESET)

        [search_strings.append(choice) for choice in answer_choices]

        search_string = ' '.join(search_strings)

        driver.switch_to.new_window('tab')
        driver.get('https://www.google.com/search?q=' + search_string)
        driver.switch_to.window(driver.window_handles[0])

    except TimeoutException:
        
        try:
            search_strings = []

            dropdown_question = waitFindElements(By.XPATH, '//form/p', parent=question_container)

            dropdown_question = [choice.text for choice in dropdown_question]
            [search_strings.append(choice) for choice in dropdown_question]
            
            print(Fore.CYAN + "    Dropdown MC detected" + Fore.RESET)

            search_string = ' '.join(search_strings)

            driver.switch_to.new_window('tab')
            driver.get('https://www.google.com/search?q=' + search_string)
            driver.switch_to.window(driver.window_handles[0])

        except TimeoutException:

            try:

                waitFindElement(By.XPATH, '//div[@class="sbgColumn leftColumn sbg2Cat"]')
                print(Fore.CYAN + "    Collumn activity detected" + Fore.RESET)  

            except TimeoutException:

                try:
                    waitFindElement(By.XPATH, '//div[@id="matchingActivity"]')
                    
                    print(Fore.CYAN + "    Matching activity detected" + Fore.RESET)

                except TimeoutException:
                    
                    try:

                        reading = waitFindElement(By.XPATH, '//div[@class="reading pane-blue"]').text
                        print(Fore.LIGHTCYAN_EX + "    Reading short answer question detected" + Fore.RESET)

                        search_strings.append('"' + reading + '"')

                    except TimeoutException:
                        pass

                    question_iframe = waitFindElement(By.XPATH, '//iframe[@id="iFramePreview"]')
                    driver.switch_to.frame(question_iframe)

                    waitFindElement(By.CLASS_NAME, 'QuestionTextArea')

                    print(Fore.CYAN + "    Short Answer Detected" + Fore.RESET)
