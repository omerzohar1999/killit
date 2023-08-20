import time
import datetime
import os

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

academic_year = int(datetime.datetime.now().strftime("%Y")) + 1
base_url = f'https://sheilta.apps.openu.ac.il/CoursesRegistration/Pages/GroupSearchResults.aspx?Semester={academic_year}'
semesters = ['%u05D0','%u05D1','%u05D2']
parameters = '&Degree=0&GeographicalArea=,01,02,03,04,05,06,07,09,&InstructionHours=00:01&Days=111111&Page=1'

chrome_options = ChromeOptions()
chrome_options.add_argument("--headless=new")
prefs = {"download.default_directory": os.getcwd(),
        "download.directory_upgrade": True,
        "download.prompt_for_download": False,}
chrome_options.add_experimental_option("prefs", prefs)


for semester in semesters:  
    driver = webdriver.Chrome(options = chrome_options)
    driver.get(base_url+semester+parameters)
    button = driver.find_element(By.ID, 'ContentPlaceHolder1_btnExcel')
    button.click()
    renamed = False
    while True:
        try:
            os.path.isfile('Excel.xls')
            os.rename('Excel.xls', f'{academic_year}_{semesters.index(semester)}.xls')
            break
        except FileNotFoundError:
            time.sleep(3)

    driver.quit()