# -*- coding: utf-8 -*-
import scrapy

from datetime import datetime


class ExtraPetiteSpider(scrapy.Spider):
    name = 'extra_petite'
    allowed_domains = ['extrapetite.com']
    start_urls = ['https://www.extrapetite.com/']

    def _get_date(self, article):
        date = article.xpath('header/span')[0].css("::text")[0].get().strip()
        # Convert article date string to YYYY/MM/DD
        return datetime.strptime(date, "%B %d, %Y").strftime("%Y/%m/%d")

    def _get_tags(self, article):
        return [t.split('tag-')[1].strip() for t in article.re('tag-.*')]

    def _get_outfits(self, article):
        outfits = article.xpath('div[@class="entry-content"]/div[@class="post-content-container"]/div[@class="post-text-content"]/div[@class="post-details"]/div[@class="outfit-box-outer"]/div[@class="outfit-box"]')
        links = outfits.css('a::attr(href)').extract()
        text = outfits.css('a::text').extract()
        for l,t in zip(links, text):
            yield {
                'link': l,
                'item': t
            }


    def parse(self, response):
        for article in response.css('article'):
            tags = self._get_tags(article)
            date = self._get_date(article)
            for outfit in self._get_outfits(article):
                outfit['tags'] = tags
                outfit['date'] = date
                yield outfit
        # for post in response.css('div.outfit-box'):
        #     links = post.css('a::attr(href)').extract()
        #     text = post.css('a::text').extract()
        #     for l,t in zip(links, text):
        #         yield {
        #             'link': l,
        #             'item': t
        #         }

        next = response.css('div.nav-pagination').css('div.rvlv_alignright').css('a::attr(href)').extract()[0]
        yield scrapy.Request(next, meta={'dont_redirect': True}, callback=self.parse)