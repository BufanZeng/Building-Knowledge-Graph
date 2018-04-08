# -*- coding: UTF-8 -*-  
# import urllib2
from lxml import etree
from selenium import webdriver  
# import os
# from selenium.webdriver.common.keys import Keys
import time
# from bs4 import BeautifulSoup
import datetime
import json

chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

d_id=1857
# driver = webdriver.Chrome()
# baseurl = "https://www.apartments.com/los-angeles-ca/"
# baseurl = "https://www.apartments.com/san-francisco-ca/"
# baseurl = "https://www.apartments.com/new-york-ny/"
baseurl = "https://www.apartments.com/seattle-wa/"
# file = open("hw2_la.txt","w") #d_id=479
# file = open("hw2_sf.txt","w") #d_id=1164
# file = open("hw2_ny.txt","w") #d_id=1857
file = open("hw2_seattle.txt","w")
for i in range (1,29):
	url = baseurl + str(i)
	driver.get(url)
	time.sleep(1)
	html = etree.HTML(driver.page_source)
	linklist = html.xpath('//*[@id="placardContainer"]/ul/li/article/header/a/@href')
	if linklist == []:
		linklist = html.xpath('//*[@id="placardContainer"]/ul/li/article/@data-url')
	for j in linklist:
		driver.get(j)
		crawltime = str(datetime.datetime.now())
		contenthtml = etree.HTML(driver.page_source)
		content = etree.tostring(contenthtml,method="html")
		d_id += 1
		d = {"doc_id":d_id, "url":j, "raw_content": content, "timestamp_crawl": crawltime}
		json_str = json.dumps(d)
		

		file.write(json_str)
		file.write("\n")
print d_id
file.close()
