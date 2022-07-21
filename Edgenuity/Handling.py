from Utils import * 

quiz_completed = False

def search(choices, search_strings):
    
    [search_strings.append(choice) for choice in choices]
    search_string = ' '.join(search_strings)

    driver.switch_to.new_window('tab')
    driver.get('https://www.google.com/search?q=' + search_string)

    driver.switch_to.window(driver.window_handles[0])
    
    try:
        switchToStage()
    except TimeoutException: ...

def switchToStage():
    driver.switch_to.default_content()
    stage_iframe = waitFindElement(By.XPATH, '//iframe[@allow]', timeout=10)
    driver.switch_to.frame(stage_iframe)

def switchToPreview():
    switchToStage()
    question_iframe = waitFindElement(By.XPATH, '//iframe[@id="iFramePreview"]')
    driver.switch_to.frame(question_iframe)

def reading( search_strings: list, parent=None ):

    try:
        reading = waitFindElement(By.XPATH, '//div[@class="reading pane-blue"]', parent=parent, timeout=.5).text
        search_strings.append(reading)

    except TimeoutException: 

        try:
            reading_element = waitFindElements(By.XPATH, '//div[@class="column"]/div/div/p', parent=parent, timeout=.5)
            reading_text = []

            [reading_text.append(prompt.text) for prompt in reading_element]

            search_strings.append(' '.join(reading_text))

        except TimeoutException: 

            try:
                reading = waitFindElements(By.XPATH, '//div[@class="column"]/div/div/p', parent=parent, timeout=.5)

                [reading.append(prompt.text) for prompt in reading]

                search_strings.append(' '.join(reading))
            except TimeoutException: ...
      
def multipleChoice( parent=None ):
    search_strings = []

    reading(search_strings=search_strings, parent=parent)

    if (parent != None):
        question_content = findElements(By.XPATH, '//div[@class="Practice_Question_Body"]', parent=parent)

        answer_choices = []

        for choice in question_content:
            if choice.text != "":
                answer_choices.append(choice.text)
        
        search_strings.append('"' + answer_choices[0] +'"')

    else: 
        question_content = waitFindElements(By.XPATH, '//div[@class="Practice_Question_Body"]')

        question = question_content[0].text

        search_strings.append('"' + question + '"')
    
        answer_choices = waitFindElements(By.XPATH, '//div[@class="answer-choice"]')
        answer_choices = [choice.text for choice in answer_choices]

    search(answer_choices, search_strings)

def dropdown( parent=None ):
    search_strings = []

    if (parent != None):
        dropdown_question = waitFindElements(By.XPATH, '//p', parent=parent)
    else:
        question_container = waitFindElement(By.XPATH, '//div[@fstack]')
        dropdown_question = waitFindElements(By.XPATH, '//form/p', parent=question_container)

    reading(search_strings=search_strings, parent=parent)

    dropdown_question = [choice.text for choice in dropdown_question]

    formatPrint("> Dropdown Question Detected")
    
    search(dropdown_question, search_strings)

def shortAnswer():
    search_strings = []

    waitFindElement(By.XPATH, '//textarea[@class="QuestionTextArea"]')

    formatPrint("> Short Answer Question Detected")

    reading(search_strings=search_strings)

    prompts = waitFindElements(By.XPATH, '//div[@class="Practice_Question_Body"]')
    prompts = [prompt.text for prompt in prompts]

    search(prompts, search_strings)

def matchingActivity():
    waitFindElement(By.XPATH, '//div[@id="matchingActivity"]')
    formatPrint("> Matching Activity Detected")

def collumnActivity():
    waitFindElement(By.XPATH, '//div[@class="sbgColumn leftColumn sbg2Cat"]')
    formatPrint("> Collumn Activity Detected")

def handleQuestion():

    try:
        
        multipleChoice()

    except TimeoutException:
        
        try:

            dropdown()

        except TimeoutException:

            try:

                shortAnswer()

            except TimeoutException:

                try:

                    matchingActivity()

                except TimeoutException:

                        try:
                            
                            collumnActivity()

                        except TimeoutException: ...

