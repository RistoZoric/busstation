from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import json

def main():
    account_url=open("account.json","r")
    account=json.load(account_url)
    email = account['email']
    password = account["password"]

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get("https://disneyworld.disney.go.com/login")


    try:
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='disneyid-iframe']")))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Username or Email Address']")))
    except Exception as e:
        pass
    username = driver.find_element(By.XPATH, "//input[@aria-label='Username or Email Address']")
    username.send_keys(f'{email}')

    try:
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='disneyid-iframe']")))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Username or Email Address']")))
    except Exception as e:
        pass
    password = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
    password.send_keys(f'{password}')

    try:
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='disneyid-iframe']")))
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Sign In']")))
    except Exception as e:
        pass

    button = driver.find_element(By.XPATH, "//button[@aria-label='Sign In']")
    button.click()


if __name__ == "__main__":
  
    main()