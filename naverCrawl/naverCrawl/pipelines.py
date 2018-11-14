# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class NavercrawlPipeline(object):
    def __init__(self):
        print("==============================pipelines start ==========================================")
        try:
            self.conn = pymysql.connect(host="kumoh42.com", user="cooperation", password="cooperation", db="newsreader",
                                        charset='utf8')
        except Exception as ex:
            print(ex)

    def process_item(self, item, spider):
        print("============================item input=========================================")
        with self.conn.cursor() as cursor:
            title = item['title']
            context = item['context']
            reporter = item['reporter']
            date = item['date']
            link = item['link']
            category = item['category']
            image = item['img']
            sql = "insert into newsreader.nr_newsdata(title,context,reporter,`date`,link,category,image) values(%s, %s, %s,%s,%s,%s,%s);"
            try:
                cursor.execute(sql, (title, context, reporter, date, link, category, image))
                self.conn.commit()
            except Exception as e:
                print(e)

        return item
