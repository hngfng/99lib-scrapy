from _cffi_backend import callback

import scrapy
from selenium import webdriver
from selenium.webdriver.common import desired_capabilities
from  selenium.webdriver.common.desired_capabilities import  DesiredCapabilities
from selenium.webdriver.firefox import options
from twisted.web import script
from  test1.items import BookItem
from scrapy.selector import Selector
from scrapy.selector import SelectorList
from scrapy.http import Request
from scrapy.http import response
from selenium.webdriver.remote import webelement
from selenium.webdriver.remote import errorhandler
from twisted.internet import defer
import sys
class Test1Spider(scrapy.Spider):
    name = "test1"
    start_urls =['http://www.99lib.net/book/index.php']
    # start_urls =['http://www.99lib.net/book/9052/index.htm']

    def parse(self, response):
        opt = webdriver.ChromeOptions()
        opt.add_argument('-headless')
        browser = webdriver.Chrome(options=opt)
        browser.get(response.url)
        lst = browser.find_elements_by_xpath("//ul[@id='list_box']/li")

        for l in lst:
            book = BookItem()
            b = l.find_element_by_xpath(".//a")
            des = l.find_elements_by_xpath(".//div[@class='intro']/p")
            desstr = ""
            for d in des:
                desstr += d.text
            IdxUrl = str(b.get_attribute("href"))
            book['title'] = "《"+str(b.get_attribute('title'))+"》"
            book['author'] = l.find_elements_by_xpath("./h4[@class='author']/a")[0].text
            book['category'] = l.find_elements_by_xpath("./h4/a")[1].text
            book['link'] = IdxUrl#str(b.get_attribute("href"))
            book['desc'] = desstr
            print(book)
            yield book
            request = scrapy.Request(IdxUrl,callback=self.parseNovel)
            # request.meta['book'] = book
            yield request
        pg = browser.find_element_by_xpath("//div[@id='right']/div[@class='dType']/div[@class='page']/a[@class='next']")
        if pg:
            nextUrl = str(pg.get_attribute("href"))
            # print(str(nextUrl))
            # yield scrapy.Request(nextUrl, callback=self.parse)
    def parseNovel(self, response):
        # book = response.meta['book']
        print("======================")
        sel = Selector(response)
        sl = sel.xpath("//div[@id='right']/dl[@id='dir']/dd/a")
        for s in sl:
            text = s.xpath("./text()").extract_first()
            # print(text)
            adUrl = s.xpath("./@href").extract_first()
            yield scrapy.Request("http://www.99lib.net"+adUrl, callback=self.parseAdapter)

    def parseAdapter(self, response):
        print(response.url+"++++++++++++++++++++++++++++++++++++++++++++++++")
        opt = webdriver.ChromeOptions()
        opt.add_argument('-headless')
        browser = webdriver.Chrome(options=opt)
        browser.get(response.url)
        browser.implicitly_wait(20)
        print(browser.page_source)
        # sel = Selector(response)
        contents = browser.find_elements_by_xpath("//div[@id='right']/div[@id='content']/div[@class]")
        print(len(contents)+"----------------------------------------------")
        idx = 0
        for c in contents:
            if idx % 5 == 0:
                # content = c.text
                print(str(c.text))
            idx += 1
        browser.close()

