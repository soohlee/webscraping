from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv
import re

driver = webdriver.Chrome(r'C:/Users/Soo/Desktop/chromedriver_win32/chromedriver.exe')
driver.get("https://www.webmd.com/vitamins/index")
wait = WebDriverWait(driver, 10)
close_popup = wait.until(EC.element_to_be_clickable((By.ID, "webmdHoverClose")))
close_popup.click()



csv_file = open('webmd_f.csv', 'w', encoding='utf-8',newline='')
writer = csv.writer(csv_file)

list_urls =[]
list_nb =[]
product_urls = driver.find_elements_by_xpath('//div[@class="vitamins-common-results"]//li')

for product_url in product_urls :
	products =product_url.find_element_by_xpath('.//a[@class="common-result-review"]').get_attribute('href')
	total = product_url.find_element_by_xpath('.//a[@class="common-result-review"]').text
	tt = total.replace("Read Reviews (","").replace(")","")
	number_pages=int(tt)//5
	list_nb.append(number_pages)
	list_urls.append(products)

list_urls_=[]
for url_,nb in zip(list_urls,list_nb):
	category_urls =['{}&pageIndex={}&sortby=3&conditionFilter=-1'.format(url_,x) for x in range(0,nb+1)] 
	list_urls_.append(category_urls)
urls = sum(list_urls_, [])

#total = driver.find_element_by_xpath('.//span[@class="totalreviews"]').text
#total = int(total.replace(" Total User Reviews",""))
#print(total)
#number_pages=total//5


for url in urls:
	driver.get(url)
#	wait_review = WebDriverWait(driver, 3)
#	reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,
#							'//div[@class="userPost"]')))
	reviews = driver.find_elements_by_xpath('//div[@class="userPost"]')

	for review in reviews:
		review_dict={}
		name = driver.find_element_by_xpath('//div[@class="tb_main"]/h1').text
		name =name.replace("User Reviews & Ratings - ","")
		reason = review.find_element_by_xpath('.//span[@class="reason"]').text
		effectiveness = review.find_element_by_xpath('.//div[@class="catRatings firstEl clearfix"]//span[@class="current-rating"]').text 
		effectiveness = effectiveness.replace("Current Rating: ","")
		easetouse = review.find_element_by_xpath('.//div[@class="catRatings clearfix"]//span[@class="current-rating"]').text
		easetouse = easetouse.replace("Current Rating: ","")
		comment = review.find_element_by_xpath('.//p[@class="comment"][1]').text.strip()
		comment = comment.split(":")[-1].strip()



		review_dict['reason'] = reason
		review_dict['name'] = name
		review_dict['effectiveness'] = effectiveness
		review_dict['easetouse'] = easetouse
		review_dict["comment"] = comment

		#review_dict["popular"] = reviewcount
		writer.writerow(review_dict.values())

	print(name)
csv_file.close()
driver.close()