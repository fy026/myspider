# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from myspider.models.es_types import TvType

from elasticsearch_dsl.connections import connections

es = connections.create_connection(TvType.Index.name, hosts=["localhost"])


def gen_suggests(index, info_tuple):
    # 根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class IjqTvInfoItem(scrapy.Item):
    tv_name = scrapy.Field()  # 电影名字
    smallImgUrl = scrapy.Field()  # 小图
    actors = scrapy.Field()  # 演员
    director = scrapy.Field()  # 导演
    editor = scrapy.Field()  # 编剧
    area = scrapy.Field()  # 地区
    language = scrapy.Field()  # 语言
    year = scrapy.Field()  # 年份
    category = scrapy.Field()  # 类别
    duration = scrapy.Field()  # 每集长度
    totalPart = scrapy.Field()  # 总集数
    updatePart = scrapy.Field()  # 已经更新的集数
    boFangTime = scrapy.Field()  # 播放时间
    dst = scrapy.Field()  # 电视台
    bfsm = scrapy.Field()  # 播放说明
    xgys = scrapy.Field()  # 相关影视
    jqjs = scrapy.Field()  # 剧情介绍
    caijiUrl = scrapy.Field()  # 采集地址
    tv_category = scrapy.Field()  #类别

    def save_to_es(self):
        tvinfo = TvType()
        if "tv_name" in self:
            tvinfo.tv_name = self['tv_name']
        if self['smallImgUrl']:
            tvinfo.small_img_url = self['smallImgUrl']
        if self['actors']:
            tvinfo.actors = self['actors']
        if self['director']:
            tvinfo.director = self['director']
        if self['editor']:
            tvinfo.editor = self['editor']
        if self['area']:
            tvinfo.area = self['area']
        if self['language']:
            tvinfo.language = self['language']
        if self['year']:
            tvinfo.year = self['year']
        if self['category']:
            tvinfo.category = self['category']
        if self['duration']:
            tvinfo.duration = self['duration']
        if self['totalPart']:
            tvinfo.total_part = self['totalPart']
        if self['updatePart']:
            tvinfo.update_part = self['updatePart']
        if self['boFangTime']:
            tvinfo.bofang_time = self['boFangTime']
        if self['dst']:
            tvinfo.dst = self['dst']
        if self['bfsm']:
            tvinfo.bfsm = self['bfsm']
        if self['xgys']:
            tvinfo.xgys = self['xgys']
        if self['jqjs']:
            tvinfo.jqjs = self['jqjs']
            # tvinfo.suggest = gen_suggests(TvType.Index.name, (tvinfo.jqjs, 10))

        tvinfo.save()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO `tv_info` (`tv_name`, `small_img_url`, `actors`, `director`, `editor`, `area`, `language`, `year`, `category`, `duration`, `total_part`, `update_part`, `bofang_time`, `dst`, `bfsm`, `xgys`, `jqjs`, `caiji_url`,`tv_category`) VALUES
             ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
        """

        for k, v in self.items():
            if k not in self or self[k] is None:
                self[k] = ""

        params = (self['tv_name'], self['smallImgUrl'], self['actors'], self['director'], self['editor'], self['area'],
                  self['language'], self['year'], self['category'], self['duration'], self['totalPart'],
                  self['updatePart'], self['boFangTime'], self['dst'], self['bfsm'], self['xgys'], self['jqjs'],
                  self['caijiUrl'],self['tv_category'])

        return insert_sql, params


class IjqTvJuqingItem(scrapy.Item):
    tv_name = scrapy.Field()  # 电影名字
    juqing = scrapy.Field()  # 剧情内容
    juqingImgs = scrapy.Field()  # 剧情图片
    jishu = scrapy.Field()  # 集数
    caijiUrl = scrapy.Field()  # 采集地址
    pass

    def get_insert_sql(self):
        for k, v in self.items():
            if k not in self or self[k] is None:
                self[k] = ""

        insert_sql = """
        INSERT INTO `tv_detail` ( `tv_name`, `juqing`, `juqingImgs`, `jisu`, `caiji_url`) VALUES ( %s, %s, %s, %s,%s);
        """
        params = (self['tv_name'], self['juqing'], self['juqingImgs'], self['jishu'], self['caijiUrl'])
        return insert_sql, params
