import time
import datetime
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import sys

from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_courses(academic_year: str):
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
                courses_by_semester.append(pd.read_html(open('Excel.xls','r', encoding='utf-8').read())[0])
                os.remove('Excel.xls')
                break
            except FileNotFoundError:
                time.sleep(3)
        driver.quit()
    return courses_by_semester

def get_prereqs(course_id):
    
    def text_between(start_marker, end_marker, text):
        pattern = re.compile(f'{re.escape(start_marker)}(.*?){re.escape(end_marker)}', re.DOTALL)
        matches = pattern.findall(text)
        return ','.join(matches)

    url_pre = 'http://www.openu.ac.il/courses/'
    url_post = '.htm'
    page = requests.get(f'{url_pre}{course_id}{url_post}').text
    prereqs = text_between(url_pre, url_post, 
                            text_between('ידע','ידע', page)
                            ).split(',')
    return prereqs


def main(academic_year):
    semesters = get_courses(academic_year)
    for semester in semesters:
        semester.drop(semester.columns[[0]], axis = 1, inplace = True)
        semester['דרישות קדם'] = semester['קורס'].apply(get_prereqs)
    return semesters

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: get_courses.py <academic_year>")
    else:
        main(sys.argv[1])