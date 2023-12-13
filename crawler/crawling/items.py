# -*- coding: utf-8 -*-

# Define here the models for your scraped items

from scrapy import Item, Field


class RawResponseItem(Item):
    appid = Field()
    crawlid = Field()
    url = Field()
    response_url = Field()
    status_code = Field()
    status_msg = Field()
    response_headers = Field()
    request_headers = Field()
    body = Field()
    links = Field()
    attrs = Field()
    success = Field()
    exception = Field()
    encoding = Field()


class ArticleItem(Item):
    id = Field()
    type = Field()
    # 渠道
    channel = Field()
    title = Field()
    # 发帖日期
    event_date = Field()
    content = Field()
    link = Field()
    # 时区
    timezone = Field()
    # 首图
    image = Field()