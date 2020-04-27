from pathlib import Path
import scrapy
import csv
import string
import os
from functools import reduce
import logging
from collections import defaultdict
import json


class MemesSpider(scrapy.Spider):
    save_path = os.getcwd()
    name = "memes"
    template_ids = dict()
    memes = defaultdict(list)

    def get_template_urls(self):
        csv_filename = reduce(os.path.join, [self.save_path, "dataset", 'popular_100_memes.csv'])
        Path(os.path.dirname(csv_filename)).mkdir(mode=0o655, parents=True, exist_ok=True)
        with open(csv_filename) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            line = 0
            for row in reader:
                line += 1
                if line == 1:
                    self.log('HEADERS\n%s %s %s' % (row[0], row[1], row[2]))
                else:
                    # self.log('%s %s %s' % (row[0], row[1], row[2]))
                    # delete punctuations
                    table = str.maketrans(dict.fromkeys(string.punctuation))
                    title = row[1].translate(table)
                    title = "-".join(title.split())
                    self.template_ids[title] = row[0]
                    yield 'https://imgflip.com/meme/' + title  # join words with -
                    #     'https://imgflip.com/meme/Distracted-Boyfriend',

    def start_requests(self):
        i = 0
        for url in self.get_template_urls():
            i = i + 1
            if i > 1:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1].split('?')[0]
        id = self.template_ids[page]
        urls = response.css('#base-left .base-unit-title a::attr(href)').extract()
        for i in urls:
            url = 'https://imgflip.com' + i
            yield scrapy.Request(url=url, callback=self.parse_meme)

        try:
            next_page = 'https://imgflip.com' + response.css('.pager .pager-next::attr(href)').extract()[0]
            yield scrapy.Request(url=next_page, callback=self.parse)
        except:
            self.save_meme(page)
            return

    def parse_meme(self, response):
        if response.css('.img-added-imgs-msg'):
            return
        title = response.css('#img-secondary .recaption::attr(href)').extract()[0].split('/')[-1]

        meme = dict()

        meme['url'] = 'https:' + response.css('#im::attr(src)').extract()[0]
        meme['post'] = response.url
        meme['metadata'] = {
            'views': response.css('.img-info .img-views::text').extract()[0].split()[0],
            'img-votes': response.css('.img-info .img-views::text').extract()[0].split()[0],
            'title': response.css('#img-title::text').extract()[0],
            'author': next(iter(response.css('.img-info .u-username::text').extract() or ''), None)
        }
        meme_title = response.css('.img-title::text').extract()
        if meme_title:
            meme['metadata']['title'] = response.css('.img-title::text').extract()[0]
        meme_author = response.css('.img-title::text').extract()
        if meme_author:
            meme['metadata']['author'] = next(iter(response.css('.img-info .u-username::text').extract() or ''), None)
        try:
            meme['boxes'] = [s.strip() for s in response.css('.img-desc::text').extract()[1].split(';')]
            self.memes[title].append(meme)
        except:
            self.log('Empty meme')

    def save_memes(self):
        for meme_name, lst in self.memes.items():
            filename = meme_name + '.json'
            path = reduce(os.path.join, [self.save_path, "dataset", "memes", filename])
            Path(os.path.dirname(path)).mkdir(mode=0o655, parents=True, exist_ok=True)

            self.log(meme_name + ' - ' + str(len(lst)), level=logging.INFO)

            with open(path, 'w+') as file:
                json.dump(lst, file, indent=2)

    def save_meme(self, meme_name):
        lst = self.memes[meme_name]
        filename = meme_name + '.json'
        path = reduce(os.path.join, [self.save_path, "dataset", "memes", filename])
        Path(os.path.dirname(path)).mkdir(mode=0o655, parents=True, exist_ok=True)

        self.log(meme_name + ' - ' + str(len(lst)), level=logging.INFO)

        with open(path, 'w+') as file:
            json.dump(lst, file, indent=2)
        del self.memes[meme_name]