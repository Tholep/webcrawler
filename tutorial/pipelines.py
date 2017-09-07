# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters  import CsvItemExporter
import datetime
class SchoolInfoPipeline(object):
	def __init__(self):
		#self.file = open("output/UK_D2"+str(datetime.datetime.now())+".csv", 'wb')
		self.file = open("output/sg"+".csv", 'wb')
		self.exporter = CsvItemExporter(self.file, unicode)
		self.exporter.start_exporting()
	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
