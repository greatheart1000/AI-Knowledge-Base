# import pandas as pd
# import numpy as np
#
# """ content=pd.read_csv(r'C:\Users\Administrator\Desktop\000002.csv',encoding='ANSI')
# # content['a']=1
# title=pd.read_csv(r'E:\nlp_pretrain_model\FinGPT-master\fingpt\FinGPT-v1\data_preparations\titles\000002.csv')
# # title['a']=1
#
# df=pd.concat([title,content],axis=1)
# df.to_csv(r'C:\Users\Administrator\Desktop\2.csv') """
#
# new_columns = ['post_user', 'post_guba', 'post_publish_time', 'post_last_time',
#        'post_display_time', 'post_ip', 'post_checkState', 'post_click_count',
#        'post_forward_count', 'post_comment_count', 'post_comment_authority',
#        'post_like_count', 'post_is_like', 'post_is_collected', 'post_type',
#        'post_source_id', 'post_top_status', 'post_status', 'post_from',
#        'post_from_num', 'post_pdf_url', 'post_has_pic',
#        'has_pic_not_include_content', 'post_pic_url', 'source_post_id',
#        'source_post_state', 'source_post_user_id', 'source_post_user_nickname',
#        'source_post_user_type', 'source_post_user_is_majia',
#        'source_post_pic_url', 'source_post_title', 'source_post_content',
#        'source_post_abstract', 'source_post_ip', 'source_post_type',
#        'source_post_guba', 'post_video_url', 'source_post_video_url',
#        'source_post_source_id', 'code_name', 'product_type', 'v_user_code',
#        'source_click_count', 'source_comment_count', 'source_forward_count',
#        'source_publish_time', 'source_user_is_majia', 'ask_chairman_state',
#        'selected_post_code', 'selected_post_name', 'selected_relate_guba',
#        'ask_question', 'ask_answer', 'qa', 'fp_code', 'codepost_count',
#        'extend', 'post_pic_url2', 'source_post_pic_url2', 'relate_topic',
#        'source_extend', 'digest_type', 'source_post_atuser',
#        'post_inshare_count', 'repost_state', 'post_atuser', 'reptile_state',
#        'post_add_list', 'extend_version', 'post_add_time', 'post_modules',
#        'post_speccolumn', 'post_ip_address', 'source_post_ip_address',
#        'post_mod_time', 'post_mod_count', 'allow_likes_state',
#        'system_comment_authority', 'limit_reply_user_auth', 'post_id',
#        'post_title', 'post_content', 'post_abstract', 'post_state']
# tt="scrapy.Field()"
# for i in new_columns:
#     i = tt
#
# import os
# print(len(os.listdir(r'E:\nlp_pretrain_model\FinGPT-master\fingpt\FinGPT-v1\data_preparations\only_content')))
import json
import random
# json_file =open(r'C:\Users\Administrator\Desktop\firefly.jsonl','w',encoding='utf-8')
# with open(r'C:\Users\Administrator\Desktop\weilidai_firefly_train.txt','r',encoding=
#           'utf-8') as f:
#     for line in f:
#         line =line.strip()
#         if "Instruction: 你现在是一个很厉害的微粒贷客服，请根据客服输入的问题进行回答" in line:
#             continue
#         else:
#             json_file.write(line+'\n')
# json_file.close()

# i=0  #15850 14265
# json_file =open(r'C:\Users\Administrator\Desktop\firefly.jsonl','r',encoding='utf-8')
# alist = [line.strip() for line in json_file]
# random.shuffle(alist)
#
file =open(r'C:\Users\Administrator\Desktop\pretrain\webank_expand.jsonl','r',encoding='utf-8')
f =open(r'C:\Users\Administrator\Desktop\pretrain\webank.jsonl','w',encoding='utf-8')
i=0
for line in file:
    line = line.strip()
    line =json.loads(line)
    context =line['context']
    target =line['target']
    data={}
    if context:
        i+=1
        data['context']= context
        data['target'] = target
        f.write(json.dumps(data,ensure_ascii=False)+'\n')
print(i)




# file2 =open(r'C:\Users\Administrator\Desktop\firefly_test.jsonl','w',encoding='utf-8')
#
# for line in alist[14265:]:
#     file2.write(line+'\n')
# file2.close()

