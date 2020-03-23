# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import re
import time
import os.path
from scrapy.exceptions import DropItem
# from scrapy.utils.response import body_or_str

class CraigslistSamplePipeline(object):
    def process_item(self, item, spider):
        return item

class EmptyDrop(object):
    def process_item(self, item, spider):
        dateFrom = time.strptime("02/08/2016","%m/%d/%Y")
        dateThis = time.strptime(item["date"],"%d %B %Y")
        if not(all(item.values())):
            raise DropItem()
        elif(dateFrom>dateThis):
            raise DropItem()
        else:
            return item

class SaveFiles(object):
    def process_item(self, item, spider):
        formatedDate = time.strptime(item["date"],"%d %B %Y")
        item["date"] = time.strftime("%d/%m/%Y", formatedDate)
        splitDate = item["date"].split('/')
        year = splitDate[2]
        month = splitDate[1]
        day = splitDate[0]
        
        name1 = item["title"][0]
        name = "".join(re.findall("[a-zA-Z0-9 ]+", name1))
        article = "\n".join(item['article'])
        save_path = os.path.join('data1', year+"-"+month+"-"+day, name+".txt")
        if not os.path.exists(os.path.dirname(save_path)):
            try:
                os.makedirs(os.path.dirname(save_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(save_path, 'a+') as f:
            f.write('name: {0} \nlink: {1}\n\n {2}'.format(name, item['link'], article.encode('utf8')))
        return item
