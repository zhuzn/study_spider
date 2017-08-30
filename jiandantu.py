#-*-coding:utf-8-*-
#Author:zhuzn
import requests
import os
import sys
import random
from bs4 import BeautifulSoup
import html5lib
import Queue
from time import ctime,sleep
reload(sys)# -*- coding:utf-8 -*-
sys.setdefaultencoding("utf-8")

#获得简单图URL
def get_jiandan_url(num1,num2):
	for n in range(num1,num2):
		s = requests.Session()
		jiandan_url = "http://jandan.net/ooxx/page-"+str(n)+"#comments"
		r = s.get(jiandan_url,headers=random.choice(headers))
		soup = BeautifulSoup(r.content,"html5lib")
		tu_url = soup.select(".view_img_link")
	for i in range(len(tu_url)):
		urls.append(tu_url[i].attrs['href'])

#打开URL，并保存到指定文件夹
def get_tu(link):
	os.chdir('E:\Pythondownload')
	s_url = 'http:'+str(j)
	print s_url
	p = requests.get(s_url,headers=random.choice(headers))
	print "pisok"
	f = open(str(j[-9:-4])+".jpg","wb")
	print "jpgisok"
	f.write(p.content)
	f.close()

if __name__ == '__main__':
	urls =[]
	headers = [
			{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
			{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
			{'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
			{'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
			{'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
			{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
	]
	num1 = int(raw_input('please input start page:'))
	num2 = int(raw_input('please input end page:'))
	get_jiandan_url(num1,num2)
	for j in urls:
		get_tu(j)
