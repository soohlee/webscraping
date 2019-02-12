from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv
import re

driver = webdriver.Chrome(r'C:/Users/Soo/Desktop/chromedriver_win32/chromedriver.exe')
driver.get('https://www.gnc.com/vitamins-supplements/')


csv_file = open('gnc_test.csv', 'w', encoding='utf-8',newline='')

writer = csv.writer(csv_file)

vita_list = driver.find_elements_by_xpath('//li[@class="expandable"]')
list_urls=[]
categories=[]
review_dict = {}
for vita in vita_list:
	category = vita.find_element_by_xpath('.//a[@class="refinement-link "]').get_attribute("href")
	category = category.replace('https://www.gnc.com/vitamins-supplements/',"").replace("/","")
	categories.append(category)
for category in categories:
	category_urls =['https://www.gnc.com/vitamins-supplements/{}/?sz=64&start={}'.format(category,x) for x in range(0,400,64)] 
	list_urls.append(category_urls)
urls = sum(list_urls, [])




for url in urls:
	driver.get(url)
	reviews = driver.find_elements_by_xpath('.//div[@class="product-tile"]')

	for review in reviews:
		cat = driver.find_element_by_xpath('.//div[@id="primary"]/h1').text
		name = review.find_element_by_xpath('.//a[@class="name-link"]').text
		rating = review.find_element_by_xpath('.//div[@class="product-review"]/span[1]').get_attribute('class')
		rating = rating.replace("TTratingBox TTrating-","").split("-")[0]
		#reviewcount = review.find_element_by_xpath('.//div[@class="product-review"]/span[2]/text()')
		price = review.find_element_by_xpath('.//span[@title="Sale Price"]').text
		price_int =float(price.replace("$",""))
		try :
			serving = review.find_element_by_xpath('.//div[@class="serving-size"]/span[2]/span[2]').text
			price_ser = round(price_int/int(serving),1)
		except:
			serving =""
			price_ser = ""


		#print(rating)
		#print(reviewcount)
		review_dict["category"] = cat
		review_dict['name'] = name
		review_dict['rating'] = rating
		review_dict['price'] = price
		review_dict['serving'] = serving
		review_dict['price_ser'] = price_ser
		#review_dict["popular"] = reviewcount
		writer.writerow(review_dict.values())

csv_file.close()
driver.close()

