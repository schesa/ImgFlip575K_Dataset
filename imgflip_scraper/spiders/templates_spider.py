from pathlib import Path
import json
import scrapy
import csv
import string
import os
from functools import reduce
import urllib.request


class TemplatesSpider(scrapy.Spider):
    save_path = os.getcwd()
    name = "templates"
    memes = dict()

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
                    url = 'https://imgflip.com/memetemplate/'
                    # delete punctuations
                    table = str.maketrans(dict.fromkeys(string.punctuation))
                    title = row[1].translate(table)
                    yield 'https://imgflip.com/memetemplate/' + "-".join(title.split())  # join words with -
                    #  example  'https://imgflip.com/memetemplate/Distracted-Boyfriend',

    def start_requests(self):
        for url in self.get_template_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
            Alternative names -> response.css('#mtm-subtitle::text').extract()[0], delete 'also called:'
            Template image url -> #mtm-img::attr(src)
            #mtm-info p -> template id, format, dimensions, file_size
            response.css('#mtm-info p::text').extract()
            ['Template ID: 112126428', 'Format: jpg', 'Dimensions: 1200x800 px', 'Filesize: 98 KB']
            [x.split(': ')[1] for x in response.css('#mtm-info p::text').extract()]
            ['112126428', 'jpg', '1200x800 px', '98 KB']
        """

        alternative_names = next(iter(response.css('#mtm-subtitle::text').extract() or []), '')
        # skip 'also called: '
        if alternative_names.startswith('also called: '):
            alternative_names = alternative_names[13:]

        mtm_info = [x.split(': ')[1] for x in response.css('#mtm-info p::text').extract()]

        page = response.url.split("/")[-1]

        template_url = 'https://imgflip.com' + response.css('#mtm-img::attr(src)').get()
        meme = self.memes.get(page, {})
        meme['title'] = response.css('#mtm-title::text').extract()[0]
        meme['template_url'] = template_url
        meme['alternative_names'] = alternative_names
        meme['template_id'] = mtm_info[0]
        meme['format'] = mtm_info[1]
        meme['dimensions'] = mtm_info[2]
        meme['file_size'] = mtm_info[3]
        self.memes[page] = meme

    def __del__(self):
        self.save_memes()

    def save_memes(self):
        for key, meme in self.memes.items():
            filename = '%s.json' % key
            path = reduce(os.path.join, [self.save_path, "dataset", "templates", filename])
            Path(os.path.dirname(path)).mkdir(mode=0o655, parents=True, exist_ok=True)
            with open(path, 'w+') as file:
                json.dump(meme, file, indent=2)
                self.save_template_img(meme)

    def save_template_img(self, meme):
        url = meme['template_url']

        img_path = reduce(os.path.join, [self.save_path, "dataset", "templates", "img", url.split('/')[-1]])
        self.log(img_path)
        Path(os.path.dirname(img_path)).mkdir(mode=0o655, parents=True, exist_ok=True)
        # Fix from https://stackoverflow.com/questions/34957748/http-error-403-forbidden-with-urlretrieve
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'meme-templates-crawler')
        opener.retrieve(url, img_path)
