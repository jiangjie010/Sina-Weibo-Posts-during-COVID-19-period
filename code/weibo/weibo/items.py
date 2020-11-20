# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WeiboUsersItem(scrapy.Item):
    weibo_id = scrapy.Field()
    gender = scrapy.Field()
    screen_name = scrapy.Field()
    follow_count = scrapy.Field()
    followers_count = scrapy.Field()
    verified_reason = scrapy.Field()
    profile_image_url = scrapy.Field()
    def get_insert_sql_and_data(self):
        insert_sql = 'INSERT INTO weibo_users(weibo_id,gender,screen_name,follow_count,followers_count,verified_reason,profile_image_url) VALUES(%s,%s,%s,%s,%s,%s,%s)'
        data = (self['weibo_id'], self['gender'] , self['screen_name'], self['follow_count'], self['followers_count'], self['verified_reason'], self['profile_image_url'])
        return (insert_sql, data)
# create table weibo_users  (weibo_id varchar(30) primary key, gender varchar(5),screen_name varchar(30),follow_count int ,followers_count int , verified_reason varchar(30),profile_image_url varchar(200))default charset=utf8mb4
class WeiboInfoItem(scrapy.Item):
    # print('**'*100)
    weibo_id = scrapy.Field()
    info_id = scrapy.Field()
    created_at = scrapy.Field()
    info = scrapy.Field()
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    def get_insert_sql_and_data(self):
        insert_sql = 'INSERT INTO weibo_infos(weibo_id,info_id,created_at,info,reposts_count,comments_count,attitudes_count) VALUES(%s,%s,%s,%s,%s,%s,%s)'
        data = (self['weibo_id'],self['info_id'],self['created_at'],self['info'],self['reposts_count'],self['comments_count'],self['attitudes_count'])
        return (insert_sql, data)

# create table weibo_infos (weibo_id varchar(30) ,info_id varchar(30) primary key ,created_at varchar(30), info text,reposts_count int,comments_count int, attitudes_count int) default charset=utf8mb4;