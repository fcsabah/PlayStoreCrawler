import scrapy
import requests
import json
import os
import time
from Similar_App_Scraper.items import SimilarAppScraperItem

class Similar_App_Spider(scrapy.Spider):
    name = "SimilarAppSpider"
    allowed_domains = ['play.google.com']
    items = []
    
    def start_requests(self):
        urls = []
        file_directory = '/home/fahad/Spyder_Projects/Similar_App_Scraper/category.txt'
        with open(file_directory) as fp:
            lines = fp.read().splitlines()
            for line in lines:
                urls.append('https://play.google.com/store/search?q=%s&c=apps' % line)
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'url':url})
            time.sleep(1)
            
    def parse(self, response):
        url = response.meta.get('url')
        # category = url.split('&')[0]
        category = url.split('=')[1].split('&')[0]
        path_to_store_image = '/home/fahad/Spyder_Projects/Similar_App_Scraper/images/' + category + '/'

        if not os.path.exists(path_to_store_image):
            os.makedirs(path_to_store_image)

        all_app = response.xpath('//*[@class="card no-rationale square-cover apps small"]')
        length = int(len(all_app))

        for i in range(length):
            item = SimilarAppScraperItem()
            item['App_ID'] = response.xpath('//*[@class="card no-rationale square-cover apps small"]/div/@data-docid')[i].extract()
            item['App_Name'] = response.xpath('//*[@class="card no-rationale square-cover apps small"]/div/div/a/@title')[i].extract()
            item['App_Icon_URL'] = response.xpath('//*[@class="card no-rationale square-cover apps small"]/div/div/div/div/div/img/@src')[i].extract()
            if 'https' not in item['App_Icon_URL']:
                item['App_Icon_URL'] = 'https:' + item['App_Icon_URL']

            image_name = path_to_store_image + item['App_ID'] +'.png'
            if os.path.exists(image_name):
                print("----------------Continue = ", item['App_ID'])
                continue

            img_data = requests.get(item['App_Icon_URL']).content
            with open(image_name, 'wb') as handler:
                handler.write(img_data)

            print("***** App_ID = ", item['App_ID'])
            self.items.append(item)

        Ajax_URL = response.xpath('//*[@class="single-title-link"]/a/@href').extract()[0]
        clp, gsr = Ajax_URL.split('&')
        clp = clp.split('=')[1]
        gsr = gsr.split('=')[1]
        Request_URL = 'https://play.google.com/store/apps/collection/search_results_cluster_apps?gsr='+ gsr +'&authuser=0'

        start = 48
        while(start <=192):
            data = 'start='+str(start)+'&num=48&numChildren=0&'
            if start == 48:
                data = data + 'pagTok=-p6BnQMCCGI=:S:ANO1ljJYYFs'
                #print("------------------for 48 ---------------------")
            elif start == 96:
                data = data + 'pagTok=-p6BnQMDCJMB:S:ANO1ljLvbuA'
                #print("------------------for 96 ---------------------")
            elif start == 144:
                data = data + 'pagTok=-p6BnQMDCMQB:S:ANO1ljIeRbo'
                #print("------------------for 144 ---------------------")
            else:
                data = data + 'pagTok=-p6BnQMDCPUB:S:ANO1ljKG00U'
                #print("------------------for 192 ---------------------")

            data = data + '&clp=' + clp + '&pagtt=3&cctcss=square-cover&cllayout=NORMAL&ipf=1&xhr=1'
            headers = {'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'}
            start = start + 48
            yield scrapy.Request(url=Request_URL, method='POST', body=data, headers=headers, callback=self.Ajax_Parse, meta={'items':self.items, 'category': category, 'start': str(start - 48)})
            time.sleep(1)
            self.items = []
        

    def Ajax_Parse(self, response):
        path_to_store_image = '/home/fahad/Spyder_Projects/PlayStoreCrawler_AI_Model_Test/images/'
        self.items = response.meta.get('items')
        category = response.meta.get('category')
        path_to_store_image = '/home/fahad/Spyder_Projects/Similar_App_Scraper/images/' + category + '/'
        start = response.meta.get('start')
        print("---------------start-------------",start)
        if not os.path.exists(path_to_store_image):
            os.makedirs(path_to_store_image)

        all_app = response.xpath('//*[@class="card no-rationale square-cover apps small"]')
        length = int(len(all_app))

        for i in range(length):
            item = SimilarAppScraperItem()
            #print("i = ", i)
            item['App_ID'] = response.xpath('//*[@class="card no-rationale square-cover apps small"]/div/@data-docid')[i].extract()
            item['App_Name'] = response.xpath('//*[@class="card no-rationale square-cover apps small"]/div/div/a/@title')[i].extract()
            item['App_Icon_URL'] = response.xpath('//*[@class="card no-rationale square-cover apps small"]/div/div/div/div/div/img/@src')[i].extract()
            if 'https' not in item['App_Icon_URL']:
                item['App_Icon_URL'] = 'https:' + item['App_Icon_URL']

            image_name = path_to_store_image + item['App_ID'] +'.png'
            if os.path.exists(image_name):
                print("----------------Continue = ", item['App_ID'])
                continue

            img_data = requests.get(item['App_Icon_URL']).content
            with open(image_name, 'wb') as handler:
                handler.write(img_data)

            print("***** App_ID = ", item['App_ID'])
            self.items.append(item)

        
        return self.items
