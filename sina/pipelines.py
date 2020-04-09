# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv,pymysql,hashlib,datetime
from w3lib.html import remove_tags
from sina.items import PostItem,CommentItem

class SQLSaveRequestPipeline(object):
    
    def process_item(self, item, spider):
        """

        :param item:
        :param spider:
        :return:
        """
        cursor = spider.connect.cursor()
        currentDT = datetime.datetime.now()
        currentDTStr = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        o = hashlib.md5(item['url'].encode("utf8")).hexdigest()
        cursor.execute("""SELECT * from tb_request where id = %s""", o)
        
        resultR = cursor.fetchone()
        if resultR:
            cursor.execute("""update tb_request set status=1, update_time=%s where id = %s """, 
                (currentDTStr, o))
            spider.connect.commit()
        else:
            cursor.execute( """insert into tb_request(
                    id,url,status,create_time,update_time
                )value ( %s,%s,1,%s,%s )""",
                ( o, item.get('url'), currentDTStr,currentDTStr ))
            spider.connect.commit()
            
        return item
    
#   def close_spider(self, spider):
#       self.connect.close()
        
class SQLSaveArticlePipeline(object):
    
    def process_item(self, item, spider):
        """

        :param item:
        :param spider:
        :return:
        """
        
        cursor = spider.connect.cursor()
        if isinstance(item, PostItem):
    #       try:
            cursor.execute("""insert into tb_article (`article_id`,`medium_id`,`url`,`author`,`subject`,`content`,`read_count`,`comment_count`,`forward_count`,`like_count`,`issue_time`,`crawl_ip`,`crawl_time`,`source`) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
                (item['article_id'],item['media_id'],item['url'],item['author'],item['subject'],item['body'],item['read_count'],item['comment_count'],item['forward_count'],item['like_count'],item['issue_time'],item['crawl_ip'],item['crawl_time'],item['source']))          
            spider.connect.commit()     
    #       except :
    #           print(cursor._last_executed)
    #           raise
        elif isinstance(item, CommentItem):
                #       try:
            cursor.execute("""insert into tb_comment (`article_id`,`content`,`issue_time`,`crawl_ip`,`crawl_time`,`reply_count`,`author`,`like_count`,`read_count`) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
                (item['article_id'],item['content'],item['issue_time'],item['crawl_ip'],item['crawl_time'],item['reply_count'],item['author'],item['like_count'],item['read_count']))           
            spider.connect.commit()     

#           cursor.execute("""SELECT * from tb_article where article_id = %s""", item['article_id'])
#       
#           resultR = cursor.fetchone()
#           if resultR:
#               cursor.execute("""update tb_article set comment_count=%s where article_id = %s """, 
#                   (item['comment_sum'], item['article_id']))
#               spider.connect.commit() 
    #       except :
    #           print(cursor._last_executed)
    #           raise
        return item
    
#   def close_spider(self, spider):
#       self.connect.close()

    
class IgnorePipeline(object):
    
    def process_item(self, item, spider):
        """

        :param item:
        :param spider:
        :return:
        """
        fields=[remove_tags(item['title']),remove_tags(item['content']),item['url']]
        with open('sohuSample1.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
