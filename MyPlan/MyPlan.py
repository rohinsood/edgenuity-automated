from Utils import *

def login():
    driver.get("https://launchpad.classlink.com/poway")

    formatPrint("Opening MyPlan", color=Fore.BLUE)

    lines = []
    with open("login.txt") as f:
        lines = f.readlines()

    USERNAME = lines[0].strip()
    PASSWORD = lines[1].strip()

    formatPrint("Logging in")

    username_input = waitFindElement(By.ID, "username")
    username_input.send_keys(USERNAME)

    password_input = waitFindElement(By.ID, "password")
    password_input.send_keys(PASSWORD)
    username_input.send_keys(Keys.RETURN)

def openEdgenuity():

    opening_string = Fore.Blue + "Opening Edgenuity\n" + Fore.WHITE+ "(Try clicking the sign in button manually if you are not logged in after a few seconds)"
    formatPrint(opening_string)

    edgenuity_link = waitFindElement(By.XPATH, '//application[@aria-label="Edgenuity (Student)"]', timeout=20)

    edgenuity_click = ActionChains(driver=driver)
    edgenuity_click.context_click(edgenuity_link).send_keys(Keys.RETURN)
    edgenuity_click.perform()
    edgenuity_click.release()

def closeMyPlan():

    formatPrint("Closing MyPlan")

    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])