# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field
from scrapy.item import Item


class HTMLItem(Item):
    """
HTML
    """

    content = Field()
    url = Field()
    extra = Field()
    
class PostItem(Item):
    """
Article
    """

    url = Field()
    author = Field()
    #文章来源
    source = Field()
    subject = Field()
    body = Field()
    read_count = Field()
    comment_count = Field()
    forward_count = Field()
    like_count = Field()
    issue_time = Field()
    crawl_ip = Field()
    crawl_time = Field()
    
    media_id = Field()
    article_id = Field()
    
class CommentItem(Item):
    """
Comment
    """

    url = Field()
    article_id = Field()
    content = Field()
    reply_count = Field()
    author = Field()
    like_count = Field()
    read_count = Field()

    issue_time = Field()
    crawl_ip = Field()
    crawl_time = Field()
    
    comment_sum = Field()

class WwwCehComCnItem(Item):

    article_id = Field()
    subject = Field()
    issue_time = Field()
    url = Field()
    author = Field()
    content = Field()