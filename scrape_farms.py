from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from webdriver_manager.chrome import ChromeDriverManager
import json

driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 10)

current_url = "https://www.workaway.info/en/hostlist?showMoreOptions=0&search=&lang=en&workawayer_capacity=0&languages=&date_start=&date_end=&min_stay=&host_rating=0&country=US&region=&gnid=334&lat=&lon=&ct=&distance="
next_page_url = "https://www.workaway.info/en/hostlist?showMoreOptions=0&search=&lang=en&workawayer_capacity=0&languages=&date_start=&date_end=&min_stay=&host_rating=0&country=US&region=&gnid=334&lat=&lon=&ct=&distance="

next_page = True

while next_page:

    current_url = next_page_url
    driver.get(current_url)

    elems = driver.find_elements_by_css_selector('#listentry-wrapper .listentry-content a')

    links_on_page = []
    for i in range(len(elems)):
        link = elems[i].get_attribute('href')
        links_on_page.append(link)

    for link in links_on_page:
        driver.get(link)
        # content = driver.find_element_by_css_selector('#mapcontainer script:nth-child(5)')
        title = driver.execute_script('return document.querySelector(".nomargin").innerText')
        html_script = driver.execute_script('return document.querySelector("#mapcontainer script:nth-child(5)").innerText')

        text_file = open('long_lat.txt', 'w')
        text_file.write(html_script)
        text_file.close()

        farm = {}
        
        with open('long_lat.txt', 'r') as read_file:
            for line in read_file:
                string = '{"lat":'
                if string in line:
                    clean_line = line.split(',')
                    farm['lat'] = float(clean_line[1].split('"')[3])
                    farm['lon'] = float(clean_line[2].split('"')[3])
                    farm['link'] = link
                    farm['title'] = title

        availability = {}
        for i in range(0, 12):
            try:
                status = driver.execute_script("return document.querySelectorAll('#section-calendar .container-fluid .hostcalmonth')[{}].querySelector('.hostcalmonthinner').firstElementChild.className".format(i)).split()[0]
            except:
                status = None
            else:    
                availability[i+1] = status

        farm['available_months'] = []

        for key, value in availability.items():
            if value == 'calendar_green':
                farm['available_months'].append(key)

        existing_data = None
        with open('data/farms.json', mode='r+', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
        
        with open('data/farms.json', mode='r+', encoding='utf-8') as json_file:
            if not existing_data:
                existing_data = []
            existing_data.append(farm)

            json.dump(existing_data, json_file)

    driver.get(current_url)
    try:
        next_page = driver.find_element_by_css_selector('.pagination-custom-next a')
    except:
        break
    else:
        # uncomment for debugging purposes
        print(next_page)
        next_page_url = next_page.get_attribute('href')
        # uncomment for debugging purposes
        print(next_page_url)



