import json
from lxml import etree
import re


i=1
out = {}
reg = re.compile("\n +",re.MULTILINE)
with open("/Users/bufan/inf558/HW/Bufan_Zeng_hw1/Bufan_Zeng_cdr.jl", "r") as f:
	
		for line in f:

			raw = json.loads(line)
			
			tree = etree.HTML(raw["raw_content"])
			try:
				if tree.xpath('//*[@id="apartmentsTabContainer"]/div/div[1]/div/table/tbody/tr/td[1]/span[@class="shortText"]/text()') != []:
					info = {
							"aptname" : reg.sub("",tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[1]/h1/text()')[0]),
							"bed" : [reg.sub("", elem) for elem in tree.xpath('//*[@id="apartmentsTabContainer"]/div/div[1]/div/table/tbody/tr/td[1]/span[@class="shortText"]/text()')],
							"bath" : [reg.sub("", elem) for elem in tree.xpath('//*[@id="apartmentsTabContainer"]/div/div[1]/div/table/tbody/tr/td[2]/span[@class="shortText"]/text()')],
							"rent" :[reg.sub("", elem) for elem in tree.xpath('//*[@id="apartmentsTabContainer"]/div/div[1]/div/table/tbody/tr/td[@class="rent"]/text()')],
							# "deposit" :tree.xpath('//*[@id="apartmentsTabContainer"]/div/div[1]/div/table/tbody/tr/td[@class="deposit"]/text()'),
							# "unit" :tree.xpath('//*[@id="apartmentsTabContainer"]/div/div[1]/div/table/tbody/tr/td[@class="unit"]/text()'),
							"sqft" :tree.xpath('//*[@id="apartmentsTabContainer"]/div/div[1]/div/table/tbody/tr/td[@class="sqft"]/text()'),
							"features": tree.xpath('//*[@id="amenitiesSection"]/div[1]/section/div[8]/ul/li/text()')
					} 
				else:
					info = {
						"aptname" : reg.sub("",tree.xpath('//*[@id="propertyHeader"]/div[1]/div[1]/div[1]/h1/text()')[0]),
						'bed' : [reg.sub("", elem) for elem in tree.xpath('//*[@id="availabilitySection"]/div[1]/table/tbody/tr/td[1]/span[3]/text()')],
						'bath' : [reg.sub("", elem) for elem in tree.xpath('//*[@id="availabilitySection"]/div[1]/table/tbody/tr/td[2]/span[3]/text()')],
						'rent' : [reg.sub("", elem) for elem in tree.xpath('//*[@id="availabilitySection"]/div[1]/table/tbody/tr/td[3]/text()')],
						'sqft' : tree.xpath('//*[@id="availabilitySection"]/div[1]/table/tbody/tr/td[@class="sqft"]/text()'),
						'features' : tree.xpath('//*[@id="amenitiesSection"]/div[1]/section/div[8]/ul/li/text()')
					}
			except:
				continue

			out[str(i)] = info
			i+=1
			# if i ==5:
			# 	break
			print info['aptname'] + " " + str(i)
with open("/Users/bufan/inf558/HW/Bufan_Zeng_hw3/Wrapper.json", "w+") as f1:
	f1.write(json.dumps(out))


