# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

new_columns = ['post_user', 'post_guba', 'post_publish_time', 'post_last_time',
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
class BbItem(scrapy.Item):
    # define the fields for your item here like:
    # for i in new_columns:
    #    i = scrapy.Field()
    text =scrapy.Field()
    post_user = scrapy.Field()
    post_guba = scrapy.Field()
    post_publish_time = scrapy.Field()
    post_last_time = scrapy.Field()
    post_display_time = scrapy.Field()
    post_id = scrapy.Field()
    post_title=scrapy.Field()
    post_content =scrapy.Field()
    post_abstract =scrapy.Field()
    post_state =scrapy.Field()
    # post_checkState = scrapy.Field()
    # post_click_count = scrapy.Field()
    # post_forward_count = scrapy.Field()
    # post_comment_count = scrapy.Field()
    # post_comment_authority = scrapy.Field()
    # post_like_count= scrapy.Field()
    # post_is_like = scrapy.Field()
    # post_is_collected = scrapy.Field()
    # post_type = scrapy.Field()
    # post_source_id  = scrapy.Field()
    # post_top_status = scrapy.Field()
    # post_status = scrapy.Field()
    # post_from = scrapy.Field()
    # post_from_num = scrapy.Field()
    # post_pdf_url= scrapy.Field()
    # post_has_pic= scrapy.Field()
    # has_pic_not_include_content= scrapy.Field()
    # post_pic_url = scrapy.Field()
    # source_post_id= scrapy.Field()
    # source_post_state= scrapy.Field()
    # source_post_user_id= scrapy.Field()
    # source_post_user_nickname= scrapy.Field()
    # source_post_user_type= scrapy.Field()
    # source_post_user_is_majia = scrapy.Field()
    # source_post_pic_url = scrapy.Field()
    # source_post_title = scrapy.Field()
    # source_post_content = scrapy.Field()
    # source_post_abstract = scrapy.Field()
    # source_post_ip = scrapy.Field()
    # source_post_type = scrapy.Field()
    # source_post_guba = scrapy.Field()
    # post_video_url = scrapy.Field()
    # source_post_video_url = scrapy.Field()
    # source_post_source_id = scrapy.Field()
    # code_name = scrapy.Field()
    # product_typev_user_code = scrapy.Field()
    # source_click_count = scrapy.Field()
    # source_comment_count = scrapy.Field()
    # source_forward_count = scrapy.Field()
    # source_publish_time  = scrapy.Field()
    # source_user_is_majia = scrapy.Field()
    # ask_chairman_state = scrapy.Field()
    # selected_post_code = scrapy.Field()
    # selected_post_name = scrapy.Field()
    # selected_relate_guba = scrapy.Field()
    # ask_question = scrapy.Field()
    # ask_answer = scrapy.Field()
    # qa = scrapy.Field()
    # fp_code = scrapy.Field()
    # codepost_count = scrapy.Field()
    # extend = scrapy.Field()
    # post_pic_url2 = scrapy.Field()
    # source_post_pic_url2 = scrapy.Field()
    # relate_topic = scrapy.Field()
    # source_extend = scrapy.Field()
    # digest_type = scrapy.Field()
    # source_post_atuser = scrapy.Field()
    # post_inshare_count = scrapy.Field()
    # repost_state = scrapy.Field()
    # post_atuser = scrapy.Field()
    # reptile_state = scrapy.Field()
    # post_add_list = scrapy.Field()
    # extend_version = scrapy.Field()
    # post_add_time = scrapy.Field()
    # post_modules = scrapy.Field()
    # post_speccolumn = scrapy.Field()
    # post_ip_address = scrapy.Field()
    # source_post_ip_address = scrapy.Field()
    # post_mod_time = scrapy.Field()
    # post_mod_count = scrapy.Field()
    # allow_likes_state = scrapy.Field()
    # system_comment_authority = scrapy.Field()
    # limit_reply_user_auth = scrapy.Field()
    # post_id = scrapy.Field()
    # post_title = scrapy.Field()
    # post_content = scrapy.Field()
    # post_abstract = scrapy.Field()
    # post_state = scrapy.Field()




