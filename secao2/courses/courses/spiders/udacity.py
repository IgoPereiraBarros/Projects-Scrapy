# -*- coding: utf-8 -*-
import scrapy


class UdacitySpider(scrapy.Spider):
    name = 'udacity'
    #allowed_domains = ['https://www.udacity.com/courses/all']
    start_urls = ['https://www.udacity.com/courses/all/']

    '''
    def parse(self, response):
        divs = response.xpath('/html/body/ir-root/ir-content/ir-course-catalog/section[3]/div[1]/div[2]/ir-course-card-catalog/div/div[1]/div[1]')

        for div in divs:
            link = div.xpath('.//h3/a')
            title = link.xpath('./text()').extract_first()
            href = link.xpath('./@href').extract_first()
            #img = div.xpath('.//img[contains(@class, "image-overlay")]/@src').extract_first()
            img = div.xpath('./div[4]/ir-catalog-card/div/div[1]/div[1]/div[1]/a/div[contains(@class, "image-container ng-star-inserted")]/@style').extract_first()
            description = div.xpath('.//div[contains(@class, "skills ng-star-inserted")]/span[contains(@class, "truncate-content")]/span[contains(@class, "ng-star-inserted")]/text()').extract()
            
            desc_join = ''.join(description[:4]) # transforma em string
            desc_split = desc_join.split(',') # dividi string pela virgula
            desc = ' '.join(desc_split) # junto toda a string separando com espaço em branco

            yield {
                'title': title,
                'url': href,
                'image': img,
                'description': desc,
            }
    '''

    def parse(self, response):
        divs = response.xpath('/html/body/ir-root/ir-content/ir-course-catalog/section[3]/div[1]/div[2]/ir-course-card-catalog/div/div[1]/div[1]')

        for div in divs:
            link = div.xpath('.//h3/a')
            href = link.xpath('./@href').extract_first()
            yield scrapy.Request(
                url='https://www.udacity.com%s' % href, 
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        title = response.xpath('//title/text()').extract_first()
        headline = response.xpath('//p[contains(@class, "hero__course--subtitle")]/text()').extract_first()
        image = response.xpath('//ir-instructor/img[contains(@class, "instructor--photo")]/@src').extract_first()

        instructors = []
        for h3 in response.xpath('//ir-instructor[contains(@class, "ng-star-inserted")]'):
            instructors.append(
                {
                    'name': h3.xpath('.//h3/text()').extract_first(),
                    'image': h3.xpath('.//img/@src').extract_first(),
                }
            )

        yield {
            'title': title,
            'headline': headline,
            'image': image,
            'instructors': instructors,
        } 