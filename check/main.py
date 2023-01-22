
import json
import os
import threading
import time as Time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
# a dictionary to convert numeric date into phonetic form
date_day = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May",
            "06": "June", "07": "July", "08": "August", "09": "September", "10": "October",
            "11": "November", "12": "December"}

class Reservation:
    """An object representation of all the information needed to search for a reservation in disney's website
    
    A reservation at disney requires a time, a party size and a date. The website returns possible reservation for a 
    specific date and time range if a reservation of the time the user chooses isn't currently available.
     
     Attributes:
         time (str): The time a user wants to eat in the specific format : HH:MM pm/am. Capitalization matters.
         date (date): The date a user wants to make a reservation for. format: DD:MM:YY
         party (str): The amount of people who will be eating at for the reservation
    
    
    """
    def __init__(self, time, date, party):
        self.time = time
        self.party = party
        self.date = date

class Restaurant:
    """Information and details about the Restaurant a user wants to make a reservation at
     
     A Restaurant at disney as a distinct website that we can use to search for reservations. This object will have a 
     list of possible reservations a user would like to make for one specific restaurant.
     
     Attributes:
         name (str): The Name of the restaurant
         reservations (:obj: `list` of :obj: `Reservation`): A list of reservation that the user is looking for
         link (str): link to the websites specific website
    
    
    """
    def __init__(self, name, link,  reservations = []):
        self.name = name
        self.reservations = reservations
        self.link = link


 
def main():
    # threading to make sure the function is running every 5 minutes
    # threading.Timer(3, main).start()

    #get credential of site
    account_url=open("account.json","r")
    account=json.load(account_url)
    email=account['email']
    password=account['password']

    print(account)
    #get restaurant data of site
    restaurant_url=open("places.json")
    restaurant=json.load(restaurant_url)

    #login 
    login_url="https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/availability-modal/"
    # site login page
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options,executable_path=ChromeDriverManager().install())

    # driver.get(login_url)

    restaurant_list = []

    # parse data and convert to objects
    for x in restaurant["places"]:
        name = x["name"]
        link = x["link"]
        # stores temp list of reservations
        reservation_list = []

        for y in x["reservations"]:
            time = y["time"]
            date = y["date"]
            party= y["party"]
            print("time:",time,"date:",date,"party:",party)
            res = Reservation(time, date, party)

            reservation_list.append(res)
        
        restaurant_list.append(Restaurant(name, link, reservation_list ))
    
    for item in restaurant_list:
        print("Booking name:",item.name)

        driver.get(item.link+"availability-modal/")
        #login
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

        password_el = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        password_el.send_keys(f'{password}')

        try:
            WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='disneyid-iframe']")))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Sign In']")))
        except Exception as e:
            pass

        button = driver.find_element(By.XPATH, "//button[@aria-label='Sign In']")
        button.click()

        #login end
        # driver.get(item.link+"availability-modal/")

        # try:
        #     # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@id='disneyid-iframe']")))
        #     button1=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//button")))
        #     print(button1)
        # except Exception as e:
        #     print("couldn't load page")
        #     continue

        # button = driver.find_element(By.XPATH,"//[@theme='primary']/button")
        # button.click()
        # get reservation
        for reservation in item.reservations:
            
            # get day and date as numbers
            arr = reservation.date.split('/')
            # turn numeric date to text
            month = date_day[arr[0]]
            day = arr[1]
            print(day,month)
            # problems consistently loading, sleeping to let the page load
            Time.sleep(1) # full sleep because the python program is going faster than the website can handle
 
            try:
                # em=WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'modal-content-0')))
                # print(em)
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='calendar-button']")))
            except Exception as e:
                pass

            # open the calender
            elm = driver.find_element(By.XPATH, "//button[@class='calendar-button']")
            elm.click()
            # get the month at the top of the calender
            elm = driver.find_element(By.XPATH, '//[@id="ui-datepicker-div"]/div/div/span[1]')
            # until we have the correct month we click the next month
            counter = 0
            while(elm.text.lower() != month.lower()):

                # reservations can't be made more than 6 months in advanced
                # the program is getting stuck and sometimes missing the proper month
                if counter > 6:
                    break
                try:
                    elm = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//finder-calendar[@iclass="calendar"]/div/div/a[1]')))
                except TimeoutException:
                    print("Couldn't click next on calender")
                    continue
                elm = driver.find_element(By.XPATH, '//finder-calendar[@class="calendar"]/div/div/a[2]')
                elm.click()
                elm = driver.find_element(By.XPATH, '//finder-calendar[@class="calendar"]/div/div/div/span[1]')
                counter += 1

            # if we have searched too far there is an error and we exit.
            if counter > 6:
                break
            # after we find the month we need to find the proper date
            # elements = driver.find_element(By.XPATH, '//finder-calendar[@class="calendar"]/table/tbody')
            # find the element of the specific date
            Time.sleep(1) # full sleep because the python program is going faster than the website can handle
            elm = driver.find_element(By.XPATH, '//finder-calendar[@class="calendar"]/div/div[2]/table/tbody/tr//a[text()=' +day +']'  )
            # click the element
            elm.click()
            # click the dropdown list:
            elm = driver.find_element(By.XPATH, '//button[@id="custom-dropdown-button"]')
            elm.click()
            # multiple ways to find the time in the DOM, the format for time has to be 'x:xx pm'/'x:xx am'

            try:
                Time.sleep(1)
                elm = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//li[@id="option-'+date+'"+]')))
                elm.click()
            except TimeoutException:
                print("Can't find reservation time")
            # click on dropdown for party size
            elm = driver.find_element(By.XPATH, '//*[@id="partySize-wrapper"]/div[1]')
            elm.click()
            # find element for party and click
            try:
                Time.sleep(1) # full sleep because the python program is going faster than the website can handle
                elm = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-value="'+reservation.party+'" and @role="option"]')))
                elm.click()
            except TimeoutException:
                print("can't select party size")

            # click submit and search
            elm = driver.find_element(By.XPATH, '//*[@id="search-time-button"]')
            elm.click()

            try:
                # search by class name
                driver.implicitly_wait(2)# needed to call sleep here, some issues on windows version on chrome
                elm = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'availability')))
                elm = driver.find_elements(By.CLASS_NAME, 'availability')

                times = []
                for e in elm:
                    times.append(e.text)

                print(restaurant.name, reservation.date, reservation.party, times)
                
            except TimeoutException:
                print("waiting too long for element/no reservation")
        # driver.implicitly_wait(109)


    account_url.close()
    restaurant_url.close()

if __name__ == "__main__":
  
    main()