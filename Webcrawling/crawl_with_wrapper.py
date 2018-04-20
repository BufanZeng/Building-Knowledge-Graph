# -*- coding: UTF-8 -*-  
# import urllib2
from lxml import etree
from selenium import webdriver  
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import string
import json
import re

chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

# west https://www.apartments.com/los-angeles-ca/?bb=v_n256kpoNoyw--0D
# dt https://www.apartments.com/los-angeles-ca/?bb=nhn6so71mNqyw--0D
# north https://www.apartments.com/los-angeles-ca/?bb=is0lm_1irN5vo8gzO
# south https://www.apartments.com/los-angeles-ca/?bb=qmw6vo1hnNo2ss90O
baseurl = "https://www.apartments.com/los-angeles-ca/"
part = ["/?bb=v_n256kpoNoyw--0D", "/?bb=nhn6so71mNqyw--0D", "/?bb=is0lm_1irN5vo8gzO", "/?bb=qmw6vo1hnNo2ss90O"]
reg = re.compile("\n +",re.MULTILINE)
out = []
ind = 0
with open("apt_features.txt","w") as file:
	file.write("id, apt, street, city, state, zipcode, soundscore, rent, tele, url\n")
	# for p in part[0:1]:
	for p in part:
		for i in range (1,29):
			print i
			url = baseurl + str(i) + p
			# print url
			# url = 'https://www.apartments.com/13/?bb=v_n256kpoNoyw--0D'
			driver.get(url)
			html = etree.HTML(driver.page_source)
			linklist = html.xpath('//*[@id="placardContainer"]/ul/li/article/header/a/@href')
			rent = [reg.sub("", elem) for elem in html.xpath('//*[@id="placardContainer"]/ul/li/article/section/div[2]/div/div[2]/span[1]/text()')]
			tele = [reg.sub("", elem) for elem in html.xpath('//*[@id="placardContainer"]/ul/li/article/section/div[2]/div/div[3]/div/span/text()')]
			if linklist == []:
				linklist = html.xpath('//*[@id="placardContainer"]/ul/li/article/@data-url')
			for j in range(len(linklist)):
				driver.get(linklist[j])
				ss = driver.find_element_by_class_name("soundScoreSummary")
				actions = ActionChains(driver)
				actions.move_to_element(ss).perform()
				time.sleep(0.5)
				tree = etree.HTML(driver.page_source)
				try:
					if tree.xpath('//*[@id="apartmentsTabContainer"]/div/div[1]/div/table/tbody/tr/td[1]/span[@class="shortText"]/text()') != []:
							apartname = reg.sub("",tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[1]/h1/text()')[0])
							street = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div[1]/h2/span[1]/text()')[0]
							city = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div[1]/h2/span[2]/text()')[0]
							state = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div[1]/h2/span[3]/text()')[0]
							zipcode = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div[1]/h2/span[4]/text()')[0]							
					else:
						apartname = reg.sub("",tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[1]/h1/text()')[0])
						
						addr = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div/h2/span/text()')
						if len(addr) == 4:
							street = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div/h2/span[1]/text()')[0]
							city = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div/h2/span[2]/text()')[0]
							state = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div/h2/span[3]/text()')[0]
							zipcode = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div/h2/span[4]/text()')[0]
						else:
							street = apartname
							city = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div/h2/span[1]/text()')[0]
							state = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div/h2/span[2]/text()')[0]
							zipcode = tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[2]/div/h2/span[3]/text()')[0]
						
					soundscore = tree.xpath('//*[@id="soundScoreSection"]/div[1]/div[1]/div[2]/text()')[0]
					out = [str(ind),apartname,street,city,state,zipcode,soundscore,rent[j].translate(None,","),tele[j],linklist[j]]
				except:
					continue

				file.write(", ".join(out).encode("utf-8") + "\n")
				ind += 1


