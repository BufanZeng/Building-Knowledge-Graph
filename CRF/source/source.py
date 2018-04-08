import json
from lxml import etree
import re
import codecs


i=1
outtext = ""
reg = re.compile("\n +|  +",re.MULTILINE)
with open("/Users/bufan/inf558/HW/Bufan_Zeng_hw1/Bufan_Zeng_cdr.jl", "r") as f:
	with open("/Users/bufan/inf558/HW/Bufan_Zeng_hw4/train_no_tags.txt", "w+") as f1:
		with open("/Users/bufan/inf558/HW/Bufan_Zeng_hw4/test_no_tags.txt", "w+") as f2:
			for line in f:

				raw = json.loads(line)
				
				tree = etree.HTML(raw["raw_content"])
				
				pet = tree.xpath('//div[./h3="Pet Policy"]/div')
				for x in pet:
					y = etree.XML(etree.tostring(x)).xpath('//text()')
					outtext += reg.sub(" ",''.join(y)) + " "
				
				
				print str(i) + raw['url']
				

				i+=1
				if i <= 101:
					f1.write(" " +outtext.encode('utf-8') +" ")
				elif i > 101 and i <=130:
					f2.write(" " +outtext.encode('utf-8') +" ")
				else:
					break
				outtext = ""
			



