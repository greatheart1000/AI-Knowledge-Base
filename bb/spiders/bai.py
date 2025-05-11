import os
import scrapy
import pandas as pd
import numpy as np
import requests
from lxml import etree
import json
from ..items import BbItem
class BaiSpider(scrapy.Spider):
    name = 'bai'
    allowed_domains = ['guba.eastmoney.com']
    start_urls = ['https://guba.eastmoney.com/']
    link_base = "https://guba.eastmoney.com/o"
    titles_path = r"E:\nlp_pretrain_model\FinGPT-master\fingpt\FinGPT-v1\data_preparations\titles"
    file_list = os.listdir(titles_path)

    def parse(self, response):

        data_path=os.path.join(self.titles_path, self.file_list[-1])
        df =pd.read_csv(data_path)
        for url in df['content link']:
            yield scrapy.Request(self.link_base+url,
                                 callback=self.parse_csdn,
                                 dont_filter=True)
    def parse_csdn(self,response):
        item = BbItem()
        res = etree.HTML(response.text)
        dfs = res.xpath("//script[1]//text()")[2][25:][:-136]
        dfs = json.loads(dfs)
        dfs = pd.Series(dfs["post"]).to_frame().T
        dfs  = dfs.to_dict()
        text = ''
        for data in res.xpath('//div[@class="stockcodec .xeditor"]//p//text()'):
            if data is None:
                print("no data")
            else:
                text += data
        item['text'] = text
        item['post_user'] = dfs['post_user']
        item['post_guba'] = dfs['post_guba']
        item['post_publish_time'] = dfs['post_publish_time']
        item['post_last_time'] = dfs['post_last_time']
        item['post_display_time'] = dfs['post_display_time']
        item['post_id'] = dfs['post_id']
        item['post_title'] = dfs['post_title']
        item['post_content'] = dfs['post_content']
        item['post_abstract'] = dfs['post_abstract']
        item['post_state'] = dfs['post_state']
        yield  item

