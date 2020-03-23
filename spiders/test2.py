from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from craigslist_sample.items import BBCItem
import scrapy
import re
import os.path
import  logging
# from scrapy.utils.response import body_or_str
#
'''
Sitemap: https://www.bbc.com/sitemaps/https-index-com-archive.xml
Sitemap: https://www.bbc.com/sitemaps/https-index-com-news.xml
'''
class MySpider(CrawlSpider):
    name = "bbc"
    allowed_domains = ["bbc.com"]
    start_urls = ["https://www.bbc.com"]
    base_url = 'https://www.bbc.com/sitemaps/https-index-com-archive.xml'

    def parse(self, response):
        href='https://www.bbc.com/sitemaps/https-sitemap-com-archive-'#79.xml
        for i in range(62,79):
            url =href+str(i+1)+'.xml'
            yield scrapy.Request(url, self.parse_url)

    # def parse_url(self, response):
    #     text =response.text
    #     file_name =response.url.split('/')[4]
    #     with open('F:\\毕业设计\\spiders\\BBCSpider-master\\sitemap\\'+file_name ,'w+') as f:
    #         f.write(text)
    # def parse(self, response):
    #     yield scrapy.Request(self.base_url, self.parse1)

    # def parse1(self, response):
    #     text =response.text
    #     url_list=[]
    #     # with open('C:\Users\lenovo\Desktop\word_freq.txt','a+',encoding='utf8') as f:
    #     #     f.write(str(response.url))
    #     nodename = 'loc'
    #     r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" % (nodename, nodename), re.DOTALL)
    #     for match in r.finditer(text):
    #         url = match.group(2)
    #         url_list.append(url)
    #     url_list.reverse()
    #     for url in url_list:
    #         yield scrapy.Request(url, self.parse_url)

    def parse_url(self,response):
        logger = logging.getLogger(__name__)
        text = response.text
        nodename = 'loc'
        r = re.compile(r"(<%s[\s>])(.*?)(</%s>)" % (nodename, nodename), re.DOTALL)
        for match in r.finditer(text):
            url = match.group(2)
            # with open(r'C:\Users\lenovo\Desktop\word_freq.txt', 'a+', encoding='utf8') as f:
            #     f.write(url+'\n')
            if re.search( r'.com/news/', url):
                # logger.warning('news/:'+url)
                #if re.search( '//profile//', url):
                yield scrapy.Request(url, self.parse_items)
            # else:
            #     logger.warning(url+" is not okay")

    # rules = (
    #     Rule(LinkExtractor(allow=('news/')), callback="parse_items", follow= True),
    # )
    #
    def parse_items(self, response):
        logger = logging.getLogger(__name__)
        hxs = Selector(response)
        items = []
        item = BBCItem()
        item["title"] = hxs.xpath('//h1/text()').extract()
        # item["title"] = "".join(item['title']).encode('utf8',errors='ignore').decode('utf8',errors='ignore')
        #//div[@class="story-body__inner"]/p/text()
        item["article"] = hxs.xpath("//*[@class='story-body']/p/text()").extract()
        # item["article"] = "".join(item['article']).encode('utf8',errors='ignore').decode('utf8',errors='ignore')#.encode('utf8')
        item["link"] = response.url
        #update-time //p[@class ='update-time']/text()2.//div[@class="date date--v2"]/text()
        item["date"] = hxs.xpath("//*[@class='date']/text()").extract_first()
        #//*[@id="main-content"]/div[2]/span/span[1]
        if item["title"] == None or item["article"] == None or item["link"] == None or item["date"] == None :
            item["article"] = hxs.xpath("//div[@class='story-body__inner']/p/text()").extract()
            item["article"] = "\n".join(item['article'])  # .encode('utf8')
            item["link"] = response.url
            item["date"] = hxs.xpath('//div[@class="date date--v2"]/text()').extract_first()
            if item["title"] == None or item["article"] == None or item["link"] == None or item["date"] == None:
                logging.warning(item["link"] + ' is not reachable')
                # with open(r'C:\Users\lenovo\Desktop\word_freq.txt', 'a+', encoding='utf8') as f:
                #     f.write(item["link"]+'\n')
            else:
                items.append(item)
                return (items)
        else:
            items.append(item)
            return (items)
    #