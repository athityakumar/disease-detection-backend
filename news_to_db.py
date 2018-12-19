import urllib2
import re
#from azure.storage.table import TableService, Entity
from bs4 import BeautifulSoup
import json

base_url = 'http://economictimes.indiatimes.com/news/economy/agriculture'

def extract_news():
	new = []
	bd = urllib2.Request(base_url, headers={'User-Agent' : "Magic Browser"}) 
	req = urllib2.urlopen(bd)
	data = BeautifulSoup(req.read(),"lxml")
	news_list = data.find_all("div", {"class":"eachStory"})
	news_data_list = data.find_all("p", {"class":""})
	news_img = data.find_all("img")[2:]
	news_imgurl = list()
	for i in range(0,10):
		news_imgurl.append("economictimes.indiatimes.com" + news_img[i]['src'])
	news_data_list = news_data_list[3:]
	pattern = re.compile('<p>(.*?)<\/p>', re.DOTALL)
	
	for i in range(0,10):
		news_data_list[i] = pattern.findall(str(news_data_list[i]))[0]

	taglines = []
	links = []
	for news in news_list:
		tag = news.find('h3')

		try:
			taglines.append(tag.find('a').text)
			links.append(base_url + '/' + tag.find('a').get('href'))
		except AttributeError:
			pass

	i=0
	news_data_list = news_data_list[:10]
	taglines = taglines[:10]
	links = links[:10]
	for tagline in taglines:
		obj = {}
		obj['headline'] = tagline
		obj['news'] = str(news_data_list[i])
		obj['link'] = str(links[i])
		obj['img_url'] = news_imgurl[i]
		new.append(obj)
		i+=1

	with open('newsdata.txt', 'w') as outfile:
		json.dump(new, 	outfile, indent=4, sort_keys=True, separators=(',', ':'))


def main():
	extract_news()
	#Add to database

if __name__ == '__main__':
	main()
