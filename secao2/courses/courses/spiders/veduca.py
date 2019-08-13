# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

from courses.items import CoursesItem, VeducaItemLoader

class VeducaSpider(scrapy.Spider):
    name = 'veduca'
    allowed_domains = ['veduca.org']
    start_urls = ['https://veduca.org/courses']

    def parse(self, response):
        course_list = response.xpath('//div[contains(@class, "course-list")]//a')
        for course_item in course_list:
        	url = course_item.xpath('.//@href').extract_first()
        	url = 'https://veduca.org%s' % url
        	yield scrapy.Request(
        		url=url,
        		callback=self.parse_detail
        	)
        next_page = response.xpath('//span[contains(@class, "next")]/a/@href').extract_first()
        if next_page:
        	self.log('PAGE: %s' % next_page)
        	url = 'https://veduca.org%s' % next_page
        	yield scrapy.Request(
        		url=url,
        		callback=self.parse
        	)

    def parse_detail(self, response):
    	loader = VeducaItemLoader(CoursesItem(), response=response)
    	#loader.default_output_processor = TakeFirst() isso já foi definido na classe VeducaItemLoader
    	loader.add_value('url', response.url)
    	loader.add_xpath('title', '//*[contains(@class, "course-title")]/text()')
    	loader.add_xpath('headline', '//*[contains(@class, "course-subtitle")]/text()')
    	loader.add_xpath('instructors', '//*[contains(@class, "author-name")]/text()')
    	loader.add_xpath(
    		'instructors_description', 
    		'//div[contains(@class, "bio")]/div/div/div/div/div[2]'
    	)
    	loader.add_xpath('lectures', '//a[contains(@class, "item")]/@href')

    	yield loader.load_item()