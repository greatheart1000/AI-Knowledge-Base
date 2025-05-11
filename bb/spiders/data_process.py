
import csv
import json
import os
# 将 csv文件保存为json 文件
csvfile_path =r'E:\nlp_pretrain_model\FinGPT-master\fingpt\FinGPT-v1\data_preparations\process'
fieldnames =['read amount','comments','title','content link','author','create time','post_user', 'post_guba', 'post_publish_time', 'post_last_time',
       'post_display_time', 'post_ip', 'post_checkState', 'post_click_count',
       'post_forward_count', 'post_comment_count', 'post_comment_authority',
       'post_like_count', 'post_is_like', 'post_is_collected', 'post_type',
       'post_source_id', 'post_top_status', 'post_status', 'post_from',
       'post_from_num', 'post_pdf_url', 'post_has_pic',
       'has_pic_not_include_content', 'post_pic_url', 'source_post_id',
       'source_post_state', 'source_post_user_id', 'source_post_user_nickname',
       'source_post_user_type', 'source_post_user_is_majia',
       'source_post_pic_url', 'source_post_title', 'source_post_content',
       'source_post_abstract', 'source_post_ip', 'source_post_type',
       'source_post_guba', 'post_video_url', 'source_post_video_url',
       'source_post_source_id', 'code_name', 'product_type', 'v_user_code',
       'source_click_count', 'source_comment_count', 'source_forward_count',
       'source_publish_time', 'source_user_is_majia', 'ask_chairman_state',
       'selected_post_code', 'selected_post_name', 'selected_relate_guba',
       'ask_question', 'ask_answer', 'qa', 'fp_code', 'codepost_count',
       'extend', 'post_pic_url2', 'source_post_pic_url2', 'relate_topic',
       'source_extend', 'digest_type', 'source_post_atuser',
       'post_inshare_count', 'repost_state', 'post_atuser', 'reptile_state',
       'post_add_list', 'extend_version', 'post_add_time', 'post_modules',
       'post_speccolumn', 'post_ip_address', 'source_post_ip_address',
       'post_mod_time', 'post_mod_count', 'allow_likes_state',
       'system_comment_authority', 'limit_reply_user_auth', 'post_id',
       'post_title', 'post_content', 'post_abstract', 'post_state']

for file in os.listdir(csvfile_path):
    csvfile = open(os.path.join(csvfile_path,file),'r', encoding='ANSI')
    jsonfile = open(os.path.join(r'E:\nlp_pretrain_model\FinGPT-master\fingpt\FinGPT-v1\data_preparations\json_file',file.split('.')[0]+'.json'), 'w', encoding='utf-8')
    reader = csv.DictReader(csvfile, fieldnames)
    for row in reader:
        json.dump(row, jsonfile, ensure_ascii=False)
        jsonfile.write('\n')
