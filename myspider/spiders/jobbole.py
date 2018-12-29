# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse

from myspider.items import IjqTvInfoItem, IjqTvJuqingItem
from w3lib.html import remove_tags
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['www.ijq.tv']
    start_urls = ['https://www.ijq.tv/']
    custom_settings = {
        "LOG_LEVEL" : 'INFO',
        # "LOG_FILE" : './logs/jobbole.log',
    }

    def parse(self, response):

        categorys = response.css("#navbox > ul> li > a")
        for category in categorys:
            cUrl = "http:" + category.css("::attr(href)").extract_first()
            cName = category.css("::text").extract_first()
            if cName == "电视剧" or cName == "电影" or cName == "影视":
                yield Request(url=cUrl, meta={"cName": cName}, callback=self.parse_category)

        # yield Request(url="https://www.ijq.tv/yingshi/list_4___2017_1.html", meta={"cName": "sdfsd"}, callback=self.parse_category)
        pass

    def parse_category(self, response):
        # tabcontentn1
        # cList = response.css("#tabcontentn1 > ul > li")

        cList = response.css("#tabcontentn1 > ul > li > div.img_show.fl > a::attr(href)").extract()
        cName = response.meta.get("cName", "")
        for cUrl in cList:
            # cUrl = c.xpath('//div[@class="img_show fl"]/a/@href').extract_first()
            # cImage = c.xpath('//div[@class="img_show fl"]/a/img/@src').extract_first()
            yield Request(url=parse.urljoin(response.url, cUrl),meta={"cName": cName}, callback=self.parse_detail)

        nextPage = response.css("#main_list > div.w750.fl > div.pages > a:nth-child(287)::attr(href)").extract_first()
        if nextPage:
            yield Request(url=parse.urljoin(response.url, nextPage),meta={"cName": cName}, callback=self.parse_category)
        pass

    def parse_detail(self, response):

        tvInfo = IjqTvInfoItem()
        tvInfo['tv_category'] = response.meta.get("cName", "")
        tvInfo['caijiUrl'] = response.url
        tvInfo['tv_name'] = response.css("#inner_nav > dl > dt::text").extract_first()
        tvInfo['smallImgUrl'] = response.css("#v-poster > img::attr(src)").extract_first()
        actors = response.css("#v-details-list > p:nth-child(2) > a::text").extract()
        if actors:
            tvInfo['actors'] = ",".join(actors)
        else:
            tvInfo['actors'] = ''
        tvInfo['director'] = response.css("#v-details-list > p:nth-child(3) > span:nth-child(2)::text").extract_first()
        tvInfo['editor'] = response.css("#v-details-list > p:nth-child(4) > span:nth-child(2)::text").extract_first()
        tvInfo['area'] = response.css("#v-details-list > p:nth-child(5) > a::text").extract_first()
        tvInfo['language'] = response.css("#v-details-list > p:nth-child(6) > span:nth-child(2)::text").extract_first()
        tvInfo['year'] = response.css("#v-details-list > p:nth-child(7) > a::text").extract_first()
        category = response.css("#v-details-list > p:nth-child(8) > a::text").extract_first()
        if category:
            tvInfo['category'] = ",".join(category)
        else:
            tvInfo['category'] = ''

        tvInfo['duration'] = response.css("#v-details-list > p:nth-child(9)::text").extract_first()
        part = response.css("#v-details-list > p:nth-child(10) > strong::text").extract()
        if part:
            tvInfo['totalPart'] = part[0]
            tvInfo['updatePart'] = part[1]
        else:
            tvInfo['totalPart'] = ''
            tvInfo['updatePart'] = ''

        tvInfo['boFangTime'] = response.css(
            "#v-details-list > p:nth-child(11) > span:nth-child(2)::text").extract_first()
        tvInfo['dst'] = response.css("#v-details-list > p:nth-child(13)::text").extract_first()
        tvInfo['bfsm'] = response.css("#v-details-list > p:nth-child(13)::text").extract_first()
        xgys = response.css("#v-details-list > p:nth-child(14) > a::text").extract()
        if xgys:
            tvInfo['xgys'] = ','.join(xgys)
        else:
            tvInfo['xgys'] = ''
        tvInfo['jqjs'] = response.css("#hutia::text").extract_first()
        yield tvInfo

        jqUrl = response.css("#inner_nav > dl > dd > ul > li:nth-child(2) > a::attr(href)").extract_first()

        yield Request(url=parse.urljoin(response.url, jqUrl), meta={"tv_name": tvInfo['tv_name']},
                      callback=self.parse_juqing)

        pass

    def parse_juqing(self, response):
        juqing = IjqTvJuqingItem()

        juqing['caijiUrl'] = response.url
        juqing['tv_name'] = response.meta.get("tv_name", "")
        juqingjs = response.css("#v-summary div:not(.list_num)").extract()
        strContent = []
        for content in juqingjs:
            strContent.append(remove_tags(content, which_ones=('div', 'a', 'img')))

        if strContent:
            juqing['juqing'] = '</br></br></br>'.join(strContent)
        else:
            juqing['juqing'] = ''
        imgUrls = response.css("#v-summary img::attr(src)").extract()
        if imgUrls:
            juqing['juqingImgs'] = '|'.join(imgUrls)
        else:
            juqing['juqingImgs'] = ''
        jishu = response.css("#v-summary > div.list_num.blue > a.active::text").extract_first()
        if jishu:
            juqing['jishu'] = jishu
            # juqing['jishu'] = re.findall(r"\d+\.?\d*", jishu)
        else:
            juqing['jishu'] = ''

        yield juqing

        nextUrl = response.css("#aNext::attr(href)").extract_first()
        if nextUrl:
            yield Request(url=parse.urljoin(response.url, nextUrl), meta={"tv_name": juqing['tv_name']},
                          callback=self.parse_juqing)


        pass
