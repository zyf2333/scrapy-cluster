# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
import json
import re

from MyScrapy.items import ArticleItem


class KempowerStoriesSpidersSpider(scrapy.Spider):
    name = 'kempower_stories'
    allowed_domains = ['kempower.com']
    start_urls = ['http://kempower.com/stories/']

    def __init__(self, *args, **kwargs):
        super(KempowerStoriesSpidersSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        try:
            # 获取data-posts属性的值
            data_posts = response.css('main#main::attr(data-posts)').get()
            # 解析JSON数组
            posts = json.loads(data_posts)
            if posts is None:
                return
            # 遍历每个文章
            for post in posts:
                id = str(post['id'])
                event_date = post['info']
                image = post['image']
                if image is not None:
                    image_url = image['src']
                data = {'id': id, 'event_date': event_date, 'image': image_url}
                if id is None:
                    continue
                # 获取详情地址
                detail_url = post['link']
                # 请求详情地址并在回调函数中处理响应
                if detail_url is not None:
                    yield scrapy.Request(detail_url, callback=self.parse_detail, meta=data)
        except Exception as e:
            self.logger.error("Error processing %s %s: %s", self.name, response.url, e)

    def parse_detail(self, response):
        item = ArticleItem()
        item['id'] = response.meta['id']
        item['type'] = 'STORIES'
        item['channel'] = 'SITE_KEMPOWER'
        item['timezone'] = 'UTC'
        item['link'] = response.url
        item['image'] = response.meta['image']

        event_date = response.meta['event_date']
        if event_date is not None and event_date != '':
            if event_date.find('•') != -1:
                event_date = event_date.split('•')[0].strip()
            item['event_date'] = datetime.strptime(event_date + " 00:00:00", '%Y-%m-%d %H:%M:%S')

        item['title'] = response.css('h1.wp-block-heading::text').get()
        content = response.css('main.entry-content.mx-auto').getall()
        html_content = ' '.join(c.strip() for c in content if c.strip())
        item['content'] = re.sub('<.*?>', '', html_content)
        yield item
