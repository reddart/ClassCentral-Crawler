# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class ClasscentralSpider(scrapy.Spider):
    name = 'classcentral'
    allowed_domains = ['class-central.com']
    start_urls = ['http://class-central.com/subjects']


    def __init__(self,subject=None):
        self.subject=subject

    def parse(self, response):
        if self.subject:
            subject_url=response.urljoin(response.xpath('.//*[contains(@title,"Programming") and @class="text--blue"]/@href').extract_first())
            yield Request(subject_url,callback=self.subject_parser)
        else:
            self.logger.info('Scraping All Sunjects')
            subjects=response.xpath('.//*[@class="text--blue"]/@href').extract()
            for subject in subjects:
                yield Request(response.urljoin(subject),callback=self.subject_parser)
    def subject_parser(self,response):
        subject=response.xpath('.//*[@class="line--large head-4 truncate"]/text()').extract()
        courses=response.xpath('.//*[@class="text--charcoal text-2 medium-up-text-1 block course-name"]')
        for course in courses:
            course_name=course.xpath('.//@title').extract()
            course_url=course.xpath('.//@href').extract_first()
            abs_course_url=response.urljoin(course_url)
            yield{
                    'Subject':subject,
                    'Course Name':course_name,
                    'Course URL':abs_course_url
                }
            next_page=response.xpath('.//*[@rel="next"]/@href').extract_first()
            next_page=response.urljoin(next_page)
        yield Request(next_page,callback=self.subject_parser)
        
