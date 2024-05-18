from time import sleep
from selenium import webdriver
from selenium.common import StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
import os


USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
URL = os.environ["URL"]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1200, 900)
driver.get(URL)

sleep(1)
login_button = driver.find_element(By.XPATH, "/html/body/div[1]/header/nav/div/a[2]")
login_button.click()

sleep(1)
username_input = driver.find_element(By.ID, "username")
username_input.send_keys(USERNAME)
password_input = driver.find_element(By.ID, "password")
password_input.send_keys(PASSWORD)
login_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
login_button.click()

sleep(15)

jobs_list = driver.find_elements(By.CSS_SELECTOR, ".scaffold-layout__list-container > li")

for job in jobs_list:
    try:
        job.click()
    except StaleElementReferenceException as error:
        print("StaleElementReferenceException")
    except ElementClickInterceptedException as error:
        print("ElementClickInterceptedException")

    sleep(1)
    save_button = driver.find_element(By.CLASS_NAME, "jobs-save-button")
    if save_button.find_element(By.CSS_SELECTOR, "span:nth-child(1)").text == "保存":
        save_button.click()
    try:
        company_link = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/div/a')
    except NoSuchElementException:
        print("No company link.")
    else:
        driver.execute_script(f"window.open('{company_link.get_attribute("href")}', '_blank');")
        driver.switch_to.window(driver.window_handles[1])

        sleep(1)
        follow_button = driver.find_element(By.CLASS_NAME, "follow")
        follow_button.click()

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

driver.quit()
