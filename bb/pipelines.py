# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
new_columns = ['post_user', 'post_guba', 'post_publish_time', 'post_last_time',
       'post_display_time', 'post_ip', 'post_checkState', 'post_click_count',
       'system_comment_authority', 'limit_reply_user_auth', 'post_id',
       'post_title', 'post_content', 'post_abstract', 'post_state']

class BbPipeline:

    def open_spider(self,spider):
        # 打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
        self.file = open('data.csv', 'w', encoding='utf-8', newline='')
        # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
        columns=['text','post_user','post_guba','post_publish_time',
        'post_last_time','post_display_time','post_id','post_title','post_content',
                              'post_abstract','post_state']
        self.writer = csv.DictWriter(self.file,fieldnames=columns )
        self.writer.writeheader()
        # titles_path = r"E:\nlp_pretrain_model\FinGPT-master\fingpt\FinGPT-v1\data_preparations\titles"
        # file_list = os.listdir(titles_path)
        # if spider.name=='bai':
        #     self.file=open('./1.txt','a+',encoding='utf-8')

    def process_item(self, item, spider):
        # if spider.name=='bai':
        #     self.file.write(str(item)+'\n')
        # return item
        """2.保存到csv """
        # writer = csv.writer(self.file)
        # self.writer.writerow([
        self.writer.writerow(item)
        return item
    def close_spider(self,spider):
        if spider.name=='bai':
            self.file.close()