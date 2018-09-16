# -*- coding: utf-8 -*-
import scrapy


class ExtraPetiteSpider(scrapy.Spider):
    name = 'extra_petite'
    allowed_domains = ['extrapetite.com']
    start_urls = ['https://www.extrapetite.com/']

    def parse(self, response):
        for post in response.css('div.outfit-box'):
            links = post.css('a::attr(href)').extract()
            text = post.css('a::text').extract()
            for l,t in zip(links, text):
                yield {
                    'link': l,
                    'item': t
                }

        next = response.css('div.nav-pagination').css('div.rvlv_alignright').css('a::attr(href)').extract()[0]
        yield scrapy.Request(next, meta={'dont_redirect': True}, callback=self.parse)