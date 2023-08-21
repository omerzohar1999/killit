import time
import datetime
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_excel_files(academic_year: str):
    base_url = 'https://sheilta.apps.openu.ac.il/CoursesRegistration/Pages/GroupSearchResults.aspx?Semester='
    semesters = ['%u05D0','%u05D1','%u05D2'] # Aleph, Beth, Gimmel
    parameters = '&Degree=0&GeographicalArea=,01,02,03,04,05,06,07,09,&InstructionHours=00:01&Days=111111'

    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    prefs = {"download.default_directory": os.getcwd(),
            "download.directory_upgrade": True,
            "download.prompt_for_download": False,}
    chrome_options.add_experimental_option("prefs", prefs)

    courses_by_semester = []

    for semester in semesters:  
        driver = webdriver.Chrome(options = chrome_options)
        driver.get(base_url+academic_year+semester+parameters)
        button = driver.find_element(By.ID, 'ContentPlaceHolder1_btnExcel')
        button.click()
        renamed = False
        while True:
            try:
                os.path.isfile('Excel.xls')
                courses_by_semester.append(pd.read_html(open('Excel.xls','r', encoding='utf-8').read()))
                os.remove('Excel.xls')
                break
            except FileNotFoundError:
                time.sleep(3)
        driver.quit()
    return courses_by_semester

if __name__ == "__main__":
	print(get_excel_files("2024")[0])
