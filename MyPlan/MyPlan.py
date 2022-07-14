from Utils import *

def login():
    driver.get("https://launchpad.classlink.com/poway")

    print(Fore.BLUE + "Opening MyPlan" + Fore.RESET)

    lines = []
    with open("login.txt") as f:
        lines = f.readlines()

    USERNAME = lines[0].strip()
    PASSWORD = lines[1].strip()

    print("Logging in")

    username_input = waitFindElement(By.ID, "username")
    username_input.send_keys(USERNAME)

    password_input = waitFindElement(By.ID, "password")
    password_input.send_keys(PASSWORD)
    username_input.send_keys(Keys.RETURN)

def openEdgenuity():

    print("Opening Edgenuity (Try clicking the sign in button manually if you are not logged in after a few seconds)")

    edgenuity_link = waitFindElement(By.XPATH, '//application[@aria-label="Edgenuity (Student)"]', timeout=10)

    edgenuity_click = ActionChains(driver=driver)
    edgenuity_click.context_click(edgenuity_link).send_keys(Keys.RETURN)
    edgenuity_click.perform()
    edgenuity_click.release()

def closeMyPlan():

    print("Closing MyPlan")

    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])