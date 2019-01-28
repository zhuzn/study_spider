# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 21:42:46 2019

@author: zhuzhengnong
"""
import re, requests, sys, os
from lxml import etree
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QCheckBox, QPushButton, QHeaderView
from PyQt5.QtGui import QPixmap
import PyQt5.uic

PICTURES_PATH = 'E:\\工作文件夹\\Python学习\\QT\\'

ui_file = 'E:\\工作文件夹\\Python学习\\QT\\untitled\\mainwindow.ui'
(class_ui, class_basic_class) = PyQt5.uic.loadUiType(ui_file)
 
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/65.0.3325.181 Safari/537.36',
    'Referer': "http://www.mzitu.com"
}
 
class Mzitu():
 
    def __init__(self, url):
        self.url = url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                   'Host': 'www.mzitu.com'}
        response = requests.get(self.url, headers = headers)
        content = BeautifulSoup(response.text, 'lxml')
        linkblock = content.find('div', class_="postlist")
        self.linklist = linkblock.find_all('li')
 
    def printli(self):
        linklist = self.linklist
        linksum = list()
 
        for link in linklist:
            url = link.a.get('href')
            picurl = link.img.get('data-original')
            linkid = re.search(r'(\d+)', url).group()
            firstspan = link.span
            titleword = firstspan.get_text()
            secondspan = firstspan.find_next_sibling('span')
            uploadtime = secondspan.get_text()
            thirdspan = secondspan.find_next_sibling('span')
            viewcount = thirdspan.get_text()
            linksum.append((linkid, titleword, uploadtime, viewcount, picurl))
        return linksum

class Window(class_basic_class, class_ui):
 
    def __init__(self):
        super(Window, self).__init__() 
        self.url = "http://www.mzitu.com/"
        self.setupUi(self)
        totlist = Mzitu(self.url).printli()
        self.tableWidget.setRowCount(len(totlist))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0, 435)
        verticalHeader = self.tableWidget.verticalHeader()
        verticalHeader.setSectionResizeMode(QHeaderView.Fixed)
        verticalHeader.setDefaultSectionSize(30)
        self.textBrowser.setOpenExternalLinks(True)  ##隐藏列表头
        self.page = 1  ##设定初始的页面数，为后面做翻页器做准备
        self.label_pagenum.setNum(self.page)  
        self.checkBoxs = [self._addCheckbox(index, item[0], item[1]) for index, item in enumerate(totlist)]
        self.pushButtons = [self._addpushButtonpic(index, item[0], item[4]) for index, item in enumerate(totlist)]
        self.pushButtons_downloads = [self._download(index, item[0]) for index, item in enumerate(totlist)]
        self.pushButton.clicked.connect(self.getSelList)
        self.pushButton_nextpage.clicked.connect(lambda: self._nextPage(1))
        self.pushButton_uppage.clicked.connect(lambda: self._nextPage(-1))
 
 
    def _addCheckbox(self, index, idd, boxtitle):
        checkBox = QCheckBox()
        checkBox.setObjectName(idd)
        checkBox.setText(boxtitle)
        self.tableWidget.setCellWidget(index, 0, checkBox) ##setCellWidget前面两个数字分别代表行和列，最后是需要关联的元素
        return checkBox
 
    def getSelList(self):
        selList = [(item.objectName(), item.text()) for item in self.checkBoxs if item.isChecked() == True]
        for item in selList:
            url = 'http://www.mzitu.com/'+item[0]
            self.textBrowser.append(item[1])
            self.textBrowser.append('<a href = %s>%s</a>' % (url, url))  ##此处输出超级链接
        return selList
 
    def _addpushButtonpic(self, index, idd, href):
        pushButton = QPushButton()
        #pushButton.setObjectName(idd)
        pushButton.setText(idd)
        self.tableWidget.setCellWidget(index, 1, pushButton)
        pushButton.clicked.connect(lambda: self._showpic(idd, href))
        return pushButton
 
    def _showpic(self, idd, href):
        pic = requests.get(href,headers=headers).content
        pixmap = QPixmap()
        pi = pixmap.loadFromData(pic)
        if pi:
            self.label.setPixmap(pixmap)
        else:
            self.label.setText('无法预览图片')
        self.show()
 
    def _nextPage(self, page):
        self.page += page
        self.label_pagenum.setNum(self.page)
        url = self.url + '/page/' + str(self.page)
        totlist = Mzitu(url).printli()
        newcheckBoxs = []
        newpushButtons = []
        newdownloads = []
        for index, item in enumerate(totlist):
            newcheckbox = self._addCheckbox(index, item[0], item[1])
            newpushbutton = self._addpushButtonpic(index, item[0], item[4])
            newdownload = self._download(index, item[0])
            newcheckBoxs.append(newcheckbox)
            newpushButtons.append(newpushbutton)
            newdownloads.append(newdownload)
        self.checkBoxs = newcheckBoxs
        self.pushButtons = newpushButtons
        self.pushButtons_downloads = newdownloads

    def _download(self,index,idd):
        url = 'http://www.mzitu.com/'+idd
        pushButton = QPushButton()
        pushButton.setObjectName('pushButton_download')
        pushButton.setText('download')
        self.tableWidget.setCellWidget(index,2,pushButton)
        pushButton.clicked.connect(lambda:self._get_pic_urls(url))

#获得该链接下的所以的图片链接
    def _get_pic_urls(self,href):
        html = requests.get(href).content
        selector = etree.HTML(html)
        page_num = int(selector.xpath('//div[@class="pagenavi"]/a/span/text()')[-2])
        self.girl_name = selector.xpath('//h2[@class="main-title"]/text()')[0]
        self.pic_urls = []
        for i in range(1, page_num+1):
            girl_pic_url = ''.join([href, '/' + str(i)])
            html = requests.get(girl_pic_url).content
            selector = etree.HTML(html)
            pic_url = selector.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
            self.pic_urls.append(pic_url)
        try:
            self._download_pic()
        except Exception as e:
            print("{}保存失败".format(self.girl_name) + str(e))       

#下载每张图片到本地
    def _download_pic(self):
        try:
            os.mkdir(PICTURES_PATH)
        except:
            pass
        girl_path = PICTURES_PATH + self.girl_name
        try:
            os.mkdir(girl_path)
        except Exception as e:
            print("{}已存在".format(self.girl_name))
        img_name = 0
        for pic_url in self.pic_urls:
            img_name += 1
            img_data = requests.get(pic_url,headers=headers)
            pic_path = girl_path + '/' + str(img_name)+'.jpg'
            if os.path.isfile(pic_path):
                print("{}第{}张已存在".format(self.girl_name, img_name))
                pass
            else:
                with open(pic_path, 'wb')as f:
                    f.write(img_data.content)
                    print("正在保存{}第{}张".format(self.girl_name, img_name))
                    f.close()
        return

 
if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    ui = Window()
    ui.show()
    sys.exit(app.exec_())
