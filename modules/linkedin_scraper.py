from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini')

login_email = config['LinkedIn']['login_email']
login_password = config['LinkedIn']['login_password']


def linkedIn_scraper(input_url):


	driver = webdriver.Chrome('C:/webdrivers/chromedriver')
	driver.get('https://www.linkedin.com/login')

	driver.find_element_by_id('username').send_keys(login_email)
	driver.find_element_by_id('password').send_keys(login_password)
	driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button').click()

	driver.get('https://www.google.com/')
	driver.find_element_by_name('q').send_keys('linkedin.com/company AND %s' %input_url,Keys.RETURN)
	driver.find_element_by_tag_name("cite").click()
	driver.get(driver.current_url + "people/")

	SCROLL_PAUSE_TIME = 3
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	    time.sleep(SCROLL_PAUSE_TIME)
	    new_height = driver.execute_script("return document.body.scrollHeight")
	    if new_height == last_height:
	        break
	    last_height = new_height

	job_titles = driver.find_elements_by_xpath('//div[@class="lt-line-clamp lt-line-clamp--multi-line ember-view"]')
	job_titles = [job.text for job in job_titles if job.text]
	job_titles = pd.DataFrame({'title':job_titles})

	return job_titles













