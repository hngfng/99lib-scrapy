import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from test1.items import BookItem
class jiujiubook(scrapy.CrawlSpider):
    name="jiujiu"
    start_urls = ['', '']
    rules = (
        # 提取匹配 'category.php' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(LinkExtractor(allow=('/book/[0-9]*/index.htm'), restrict_xpaths= ("//ul[@id='list_box']/li/a/@href"))),

        # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
        Rule(LinkExtractor(allow=('/book/[0-9]*/[0-9]*.htm',)), callback='parse_item'),
    )
    items = []
    def parse_item(self,response):
        print(response)

