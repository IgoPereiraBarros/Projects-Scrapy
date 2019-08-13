# -*- coding: utf-8 -*-
import scrapy


class CourseraSpider(scrapy.Spider):
    name = 'coursera'
    #allowed_domains = ['https://www.coursera.org/']
    #start_urls = ['https://www.coursera.org/browse']
    category = None
    # $ scrapy crawl coursera -a category=computer-science

    def start_requests(self):
        if self.category is None:
            yield scrapy.Request(
                url='https://www.coursera.org/browse',
                callback=self.parse
            )
        else:
            yield scrapy.Request(
                url='https://www.coursera.org/browse{}'.format(self.category),
                callback=self.parse_category

            )

    def parse(self, response):
        categories = response.xpath('//div[contains(@class, "rc-DonainNav")]/a')
        for cat in categories:
            cat_url = cat.xpath('./@href').extract_first()
            self.log('Category: {}'.format(cat_url))
            yield scrapy.Request(
                url='https://www.coursera.org%s' % cat_url,
                callback=self.parse_category
            )


    def parse_category(self, response):
        #self.log(response.xpath('//title/text()').extract_first())
        courses = response.xpath('//a[contains(@class, "rc-OfferingCard")]')
        for course in courses:
            course_url = course.xpath('./@href').extract_first()
            yield scrapy.Request(
                url='https://www.coursera.org%s' % course_url,
                callback=self.parse_course
            )

    def parse_course(self, response):
        yield {
            'title': response.xpath('//title/text()').extract_first()

        }