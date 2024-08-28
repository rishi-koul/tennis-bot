import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 

chrome_options = Options()
chrome_options.add_argument("--incognito")

service = Service("./chromedriver")
driver = webdriver.Chrome(service=service)

date_today = datetime.today().strftime("%-m/%d/%Y")

date_two = datetime.today() + timedelta(days=2)
date_two = date_two.strftime("%-m/%d/%Y")

driver.get("https://www.buildinglink.com/v2/tenant/amenities/NewReservation.aspx?from=1&amenityId=" + 
           os.getenv("TENNIS_AMENTIY_ID") + "&starts=" + date_two + "%204:00:00%20PM&ends=" + date_today + "%205:00:00%20PM")

# Make sure we are at the login page
WebDriverWait(driver, 5).until(
    EC.presence_of_all_elements_located((By.ID, "UserName"))
)
# Enter login details
login_element = driver.find_element(By.ID, "UserName")
login_element.send_keys(os.getenv("USERNAME"))

password_element = driver.find_element(By.ID, "Password")
password_element.send_keys(os.getenv("PASSWORD"))

login_button = driver.find_element(By.ID, "LoginButton")
login_button.click()

# open the date picker
date_picker = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_StartTimePicker_dateInput")
date_picker.send_keys("value", "5:00")

# select 5pm as time
five_pm = driver.find_element(By.XPATH, "//*[contains(text(), '5:00 PM')]")
five_pm.click()

if(not driver.find_elements(By.XPATH, "//*[contains(text(), 'I agree to the above')]")):
    pass
else:
    terms = driver.find_element(By.XPATH, "//*[contains(text(), 'I agree to the above')]/ancestor::span/span/input")
    terms.click()


# Need to double check the time is correct, date is always correct
save_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Save')]/ancestor::a")
save_button.click()

driver.quit()

