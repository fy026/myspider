# -*- coding: utf-8 -*-
__author__ = 'bobby'


from elasticsearch_dsl import DocType, analyzer, Completion, Keyword, Text, Integer
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


# class CustomAnalyzer(_CustomAnalyzer):
#     def get_analysis_definition(self):
#         return {}


# ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class TvType(DocType):

    # suggest = Completion(analyzer=ik_analyzer)
    tv_name = Keyword()
    small_img_url = Keyword()
    actors = Text()
    director = Text()
    editor = Text()
    area = Text()
    language = Text()
    year=Integer()
    category=Text()
    duration=Keyword()
    total_part=Integer()
    update_part=Integer()
    bofang_time=Keyword()
    dst=Text()
    bfsm=Text()
    xgys=Text()
    # jqjs=Text(analyzer='ik_max_word')
    jqjs=Text()
    class Index:
        name = 'ijqtv'
    # class Meta:
    #     index = "ijqtv"
    #     doc_type = "tvinfo"

if __name__ == "__main__":
    TvType.init()
