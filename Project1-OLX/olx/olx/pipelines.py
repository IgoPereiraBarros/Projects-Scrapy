# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import pymongo

class OlxSqlitePipeline(object):

    def process_item(self, item, spider):
        self.conn.execute(
        	"INSERT INTO cars(title, categorical , model , motor_power, doors, plate_end, type_vehicle, year, fuel, mileage, exchange, direction, color, only_owner, accept_exchanges, options) VALUES (:title, :categorical , :model , :motor_power, :doors, :plate_end, :type_vehicle, :year, :fuel, :mileage, :exchange, :direction, :color, :only_owner, :accept_exchanges, :options)",
        	item
        )
        self.conn.commit()
        return item

    def create_table(self):
    	result = self.conn.execute(
    		'SELECT name FROM sqlite_master WHERE type="table" and name="cars"'
    	)
    	try:
    		value = next(result)
    	except StopIteration as e:
    		self.conn.execute(
    			"CREATE TABLE cars(id INTEGER PRIMARY KEY, title TEXT, categorical TEXT, model TEXT, motor_power TEXT, doors TEXT, plate_end TEXT, type_vehicle TEXT, year TEXT, fuel TEXT, mileage TEXT, exchange TEXT, direction TEXT, color TEXT, only_owner TEXT, accept_exchanges TEXT, options TEXT)"
    		)

    def open_spider(self, spider):
    	self.conn = sqlite3.connect('db.sqlite3')
    	self.create_table()


    def close_spider(self, spider):
    	self.conn.close()


class MongoPipeline(object):

	collection_name = 'cars'

	def __init__(self, mongo_uri, mongo_db):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mongo_uri = crawler.settings.get('MONGO_URI'),
			mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
		)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		self.db[self.collection_name].insert_one(dict(item))
		return item