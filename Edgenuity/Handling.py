from Utils import * 

def search(choices, search_strings):
    
    [search_strings.append(choice) for choice in choices]
    search_string = ' '.join(search_strings)

    driver.switch_to.new_window('tab')
    driver.get('https://www.google.com/search?q=' + search_string)

    driver.switch_to.window(driver.window_handles[0])

def switchToStage():
    driver.switch_to.default_content()
    stage_iframe = waitFindElement(By.XPATH, '//iframe[@allow]', timeout=10)
    driver.switch_to.frame(stage_iframe)

def reading( search_strings: list ):
    try:
        reading = waitFindElement(By.XPATH, '//div[@class="reading pane-blue"]').text

        search_strings.append(reading)

    except TimeoutException: 

        try:
          reading = waitFindElements(By.XPATH, '//div[@class="column"]/div/div/p')

          [reading.append(prompt.text) for prompt in reading]

          search_strings.append(' '.join(reading))

        except TimeoutException: ...
      
def multipleChoice():
    search_strings = []

    question_container = waitFindElement(By.XPATH, '//div[@fstack]')

    try:
      reading = waitFindElement(By.XPATH, '//div[@class="reading pane-blue"]', parent=question_container).text
      print(Fore.LIGHTCYAN_EX + "    Reading MC question detected" + Fore.RESET)

      search_strings.append(reading)

    except TimeoutException:
      pass

    question_content = waitFindElements(By.XPATH, '//div[@class="Practice_Question_Body"]', parent=question_container)
    question = question_content[0].text

    search_strings.append('"' + question + '"')
  
    answer_choices = waitFindElements(By.XPATH, '//div[@class="answer-choice"]', parent=question_content[1])
    answer_choices = [choice.text for choice in answer_choices]

    search(answer_choices, search_strings)

def dropdown():
    search_strings = []

    question_container = waitFindElement(By.XPATH, '//div[@fstack]')

    dropdown_question = waitFindElements(By.XPATH, '//form/p', parent=question_container)

    reading(search_strings=search_strings)

    dropdown_question = [choice.text for choice in dropdown_question]

    print(Fore.CYAN + "    Dropdown MC detected" + Fore.RESET)
    
    search(dropdown_question, search_strings)

def shortAnswer():
    search_strings = []

    waitFindElement(By.XPATH, '//textarea[@class="QuestionTextArea"]')

    reading(search_strings=search_strings)

    prompts = waitFindElements(By.XPATH, '//div[@class="Practice_Question_Body"]')
    prompts = [prompt.text for prompt in prompts]

    print(Fore.CYAN + "    Short Answer Detected" + Fore.RESET)

    search(prompts, search_strings)

def matchingActivity():
  waitFindElement(By.XPATH, '//div[@id="matchingActivity"]')
  print(Fore.CYAN + "    Matching activity detected" + Fore.RESET)

def collumnActivity():
  waitFindElement(By.XPATH, '//div[@class="sbgColumn leftColumn sbg2Cat"]')
  print(Fore.CYAN + "    Collumn activity detected" + Fore.RESET)  

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

