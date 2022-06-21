from Utils import *

def login():
    driver.get("https://launchpad.classlink.com/poway")

    lines = []
    with open("login.txt") as f:
        lines = f.readlines()

    USERNAME = lines[0].strip()
    PASSWORD = lines[1].strip()

    username_input = waitFindElement(By.ID, "username")
    username_input.send_keys(USERNAME)

    password_input = waitFindElement(By.ID, "password")
    password_input.send_keys(PASSWORD)

    password_input.send_keys(Keys.RETURN)

def openEdgenuity():
    edgenuity_link = waitFindElement(By.XPATH, '//application[@aria-label="Edgenuity (Student)"]')

    edgenuity_click = ActionChains(driver=driver)
    edgenuity_click.context_click(edgenuity_link).send_keys(Keys.RETURN)
    edgenuity_click.perform()
    edgenuity_click.release()

def closeMyPlan():
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])