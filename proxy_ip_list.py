#-*-coding:utf-8-*-
import random
from bs4 import BeautifulSoup
import html5lib
import requests


def get_xicidaili_url(num):
    xicidaili_urls = []
    for i in range(1,num):
        xicidaili_url = 'http://www.xicidaili.com/nn/' + str(i)
        xicidaili_urls.append(xicidaili_url)
    return xicidaili_urls

def get_ip_list(headers):
    ip_list = []
    for i in xicidaili_urls:
        url = i
        web_data = requests.get(url,headers=headers)
        soup = BeautifulSoup(web_data.text,"html5lib")
        ips = soup.find_all('tr')
        for i in range(1,len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[1].string +':' + tds[2].string)
        return ip_list

def get_availble_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    for i in proxy_list:
        try:
            url = "http://ip.chinaz.com/getip.aspx"
            f = open("/home/zhuzn/pythondownload/ip.txt","a+")
            res = requests.get(url,proxies = {'http':i})
            f.write(i+'\n')
        except Exception,e:
           # print "无效ip！"
            continue
            f.close()

if __name__ == '__main__':
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    num = int(raw_input('please a number:'))
    xicidaili_urls = get_xicidaili_url(num)
    ip_list = get_ip_list(headers=headers)
    get_availble_ip(ip_list)

                                                                                                                                                      1,5           Top
