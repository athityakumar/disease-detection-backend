
import urllib2
import re
#from azure.storage.table import TableService, Entity
from bs4 import BeautifulSoup
import json

base_url = 'http://kisaankranti.com/'
params = ['fertilizer', 'pesticide', 'seeds']

def extract_products():
	
	k=1
	price = []
	for param in params:	
		url = base_url + param + '.html'
		bd = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
		req = urllib2.urlopen(bd)
		data = BeautifulSoup(req.read(),"lxml")
		image_area = data.find_all("div", {"class":"product-image-area"})
		image_urls = list()
		for i in range(0, len(image_area)):
			image_urls.append(image_area[i].find_all("img")[0]['src'])
		details_area = data.find_all("div",{"class":"details-area"})
		products = [] 
		prices = []
		links = []
		for detail in details_area:
			products.append(str(detail.find("h2", {"class":"product-name"}).text))
			atag =  detail.find("h2", {"class":"product-name"}).findAll('a')
			for link in atag:
				links.append(link.get('href'))
			prices.append(detail.find("span", id=lambda x: x and x.startswith('product-')).text)

		for i in range(0,len(prices)):
			prices[i] = re.sub('\s+','',prices[i])
			prices[i] = str(re.sub(r'[^\x00-\x7F]+','', prices[i]))

		m=0
		for product in products:
			obj = {}
			obj['producttype'] = param
			obj['productname'] = str(product)
			obj['pricet'] = "Rs " + prices[m]
			obj['link'] = links[m]
			obj['image_url'] = image_urls[m]
			price.append(obj)
			m+=1
			k+=1
			
	with open('pricedata.txt', 'w') as outfile:
		json.dump(price, 	outfile, indent=4, sort_keys=True, separators=(',', ':'))


def main():
	extract_products()

if __name__ == '__main__':
	main()
