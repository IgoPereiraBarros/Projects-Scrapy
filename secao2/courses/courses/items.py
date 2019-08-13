# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from w3lib.html import remove_tags

import scrapy
from scrapy.loader.processors import Join, TakeFirst, MapCompose
from scrapy.loader import ItemLoader


class VeducaItemLoader(ItemLoader):

	default_output_processor = TakeFirst()

	instructors_description_in = MapCompose(remove_tags, str.strip)
	

class CoursesItem(scrapy.Item):

	title = scrapy.Field()
	headline = scrapy.Field()
	url = scrapy.Field()
	instructors = scrapy.Field()
	instructors_description = scrapy.Field()
	lectures = scrapy.Field(
		output_processor=Join(' | ')
	)
	image = scrapy.Field()
