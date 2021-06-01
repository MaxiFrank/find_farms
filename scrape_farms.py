from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from webdriver_manager.chrome import ChromeDriverManager
import json

driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 10)
# driver.get("https://www.workaway.info/")
# driver.find_element_by_class_name('dropdown').click()
# driver.find_element_by_css_selector('[data-target]').click()


# # why is the submit button not working?
# print(driver.find_element_by_css_selector('[data-action]'))
# css = driver.find_element_by_css_selector('[data-action]')
# class_ = driver.find_element_by_class_name('btn-modal-login')
# print(css)
# print(class_)
# class_.click()
# print(data_action.text)
# print(dir(data_action))
# driver.find_element_by_css_selector('[data-action]').submit()
# driver.quit()

# data_action = driver.find_element_by_id('loginElementsForm')
# print(data_action.text)
# print(dir(data_action))
# data_action.submit()

# # link below doesn't work
# # driver.find_element_by_xpath("//a[@href='/en/hostlist']").click()
# # driver.find_element_by_css_selector('[href^=https://www.workaway.info/en/hostlist]').click()
# driver.quit()

# driver.get("https://www.workaway.info/en/hostlist")
# select_country = driver.find_element_by_id('typeahead')
# select_country.send_keys('United States')

# need need to select the pre tag after typing in United States
# select_us = driver.find_element_by_tag_name('pre')
# print(select_us)
# select_us.click()
# show_results = driver.find_element_by_id('searchformsubmitbtn')
# show_results.click()

driver.get("https://www.workaway.info/en/hostlist?showMoreOptions=0&search=&lang=en&workawayer_capacity=0&languages=&date_start=&date_end=&min_stay=&host_rating=0&country=US&region=&gnid=334&lat=&lon=&ct=&distance=&Page=2")

elems = driver.find_elements_by_css_selector('#listentry-wrapper .listentry-content a')
for i in range(len(elems)):
    # print(elems[i].get_attribute('href'))
    print(i)
    # print(elems[5].get_attribute('href'))
    # print(elems[5].get_attribute('href'))
    link = elems[0].get_attribute('href')
    # link = elems[0].get_attribute('href')
    driver.get(link)
    # driver.find_element_by_css_selector('.nav-collapse .details [data-target]').submit()
    content = driver.find_element_by_css_selector('#mapcontainer script:nth-child(5)')
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

    availability = {}
    for i in range(0, 12):
        # mnth = driver.execute_script("return document.querySelectorAll('#section-calendar .container-fluid .hostcalmonth')[{}].innerText".format(i))
        # status = driver.execute_script("return document.querySelectorAll('#section-calendar .container-fluid .hostcalmonth')[{}].querySelector('.hostcalmonthinner').firstElementChild.className".format(i)).split()[0]
        # print(str)
        status = driver.execute_script("return document.querySelectorAll('#section-calendar .container-fluid .hostcalmonth')[{}].querySelector('.hostcalmonthinner').firstElementChild.className".format(i)).split()[0]
        availability[i+1] = status

    farm['available_months'] = []

    for key, value in availability.items():
        if value == 'calendar_green':
            farm['available_months'].append(key)
    
    jsonified_farm = farm

    # append jsonified_farm to farms.json

# print(farm)
# print(content)
# print(type(html_script))
# print(dir(content.get_attribute('value')))
# print(content.text)
# print(elems[0].get_attribute('href'))
# print(elems[1].get_attribute('href'))
# print(elems[2].get_attribute('href'))
# print(elems[3].get_attribute('href'))
# for elem in elems:
#     print(elem.get_attribute('href'))





# elems = driver.find_elements_by_xpath("//a[@href]")
# for elem in elems:
#     print(elem.get_attribute("href"))

# just need to loop through the availablity section now...