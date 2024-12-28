# Importaning necessey liberaries
from scrapy.spiders import SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy.spiders
import time
import random
import csv
from colorama import Fore,Style

# Sitemap Spider
class ScrapuniSpider(SitemapSpider):
    name = "scrapuniurl"
    allowed_domains = ["www.westminster.ac.uk"]
    url_searcher = []

    def start_requests(self):
        start_urls ="https://www.westminster.ac.uk/sitemap.xml?page=1"
        yield scrapy.Request(url=start_urls, callback=self.parse)
    
    def parse(self, response):
        links_next = []
        counter=0
        response.selector.register_namespace('d', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        for i in response.xpath('//d:loc/text()').getall():
            links_next.append(str(i))
            with open("links.txt",'a') as f:
                f.write(i)
                f.write("\n")
            self.log(i)
            

        
# Data extractor crawler
class ScrapuniSpider(SitemapSpider):
    name = "scrapunidata"
    allowed_domains = ["www.westminster.ac.uk"]
    course_data = 'Course_Data.csv'
    other_data = 'Other_Data.csv'
        
    with open(course_data, "a", encoding="utf-8") as f:
        f.write(f"Page title,UK Fees,International Fees,Duration,Campus,description,Url\n")
    with open(other_data, "a", encoding="utf-8") as f:
        f.write(f"Page title,description,Url\n")
    

    def start_requests(self):
        urls = []
        
        path = 'D:\\MSC-DATA-SCIENCE\\Msc project\\Data collection\\scraped_links.txt'
        
        with open(path, "r") as f:
            urls = f.readlines()
        
        for start_urls in urls:
            yield scrapy.Request(url=start_urls, callback=self.parse)
    
    def parse(self, response):
        text = ''
        def filter_and_write_course(title, list2):
            flag =False
            sentence = {}
            for i, item in enumerate(list2[:100]):
                if item == 'UK Fees':
                    flag = True
                    sentence.update({"UK Fees": list2[i+1]}) 
                    
                elif item == 'International Fees':
                    flag = True
                    sentence.update({"International Fees": list2[i+1]})
                    
                elif item == 'Duration':
                    flag = True
                    sentence.update({"Duration": list2[i+1]})
                    
                elif item == 'Campus':
                    flag = True
                    sentence.update({"Campus": list2[i+1]})
                    
                elif item == 'Course summary':
                    flag = True
                    sentence.update({"description": list2[i+1]})
                    
            if not flag:
                sentence.update(
                    {"Page title": title,
                    "description": " ".join(list2),
                    "UK Fees": '',
                    "International Fees": '',
                    "Duration": '',
                    "Campus": ''
                    })
            else:

                sentence.update({"Page title": title})
            
            return sentence

        
        title = response.xpath('/html/head/title/text()').get()

        print(Fore.GREEN,"********* New Page Found **********")
        print(Style.RESET_ALL)
        self.log(f'{Fore.GREEN} {title}')

        element = response.css('#main-content')
        if element:
            text = element.css('::text').getall()
            text = [item.strip() for item in text if item.strip()]
            
        if len(text) == 0:
            element = response.css('.region-content p::text').getall()
            text = [item.strip() for item in element if item.strip()]
        
        main_data = filter_and_write_course(title, text)
        main_data.update({"Url": response.url})

        if main_data["UK Fees"] != '' :    
            print(Fore.YELLOW+"This is a Course Page Updating Course_Data.csv file")
            print(Style.RESET_ALL)
            with open(self.course_data, "a", encoding="utf-8",newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    str(main_data["Page title"]),
                    str(main_data["UK Fees"]),
                    str(main_data["International Fees"]),
                    str(main_data["Duration"]),
                    str(main_data["Campus"]),
                    str(main_data["description"]),
                    str(main_data["Url"])])
                
        else:
            print(Fore.BLUE+"This is not a Course Page Updating Other_Data.csv file")
            print(Style.RESET_ALL)
            with open(self.other_data, "a", encoding="utf-8",newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    str(main_data["Page title"]),
                    str(main_data["description"]),
                    str(main_data["Url"])])        