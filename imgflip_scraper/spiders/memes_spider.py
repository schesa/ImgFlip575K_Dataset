import json
import scrapy
import csv
import string
import os
import shutil
from functools import reduce
import urllib.request


class MemesSpider(scrapy.Spider):
    name = "memes"
    memes = dict()

    def get_template_urls(self):
        csv_filename = 'popular_100_memes.csv'
        with open(csv_filename) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            line = 0
            for row in reader:
                line += 1
                if line == 1:
                    self.log('HEADERS\n%s %s %s' % (row[0], row[1], row[2]))
                else:
                    # self.log('%s %s %s' % (row[0], row[1], row[2]))
                    url = 'https://imgflip.com/memetemplate/'
                    # delete punctuations
                    table = str.maketrans(dict.fromkeys(string.punctuation))
                    title = row[1].translate(table)
                    yield 'https://imgflip.com/memetemplate/' + "-".join(title.split())  # join words with -
                    #     'https://imgflip.com/memetemplate/Distracted-Boyfriend',

    def start_requests(self):
        for url in self.get_template_urls():
            yield scrapy.Request(url=url, callback=self.parse)
            # yield scrapy.Request(url=url.replace('memetemplate', 'memegenerator', 1), callback=self.parse_generator)

    # TODO get list of bounding boxes from /memegenerator/
    #  -> #mm-preview .drag-box reverse order -> style x:left y:top width, height
    #  -> #mm-font-options .color-btn font & outline style
    # def parse_generator(self, response):
    #     self.log('')

    def parse(self, response):
        """
            DONE Alternative names -> response.css('#mtm-subtitle::text').extract()[0], delete 'also called:'
            DONE Template image url -> #mtm-img::attr(src)
            DONE #mtm-info p -> template id, format, dimensions, file_size
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
        # self.log('meme %s' % page)
        # self.log('Created File %s' % filename)
        # yield meme

    def __del__(self):
        self.save_memes()

    def save_memes(self):
        for key, meme in self.memes.items():
            save_path = 'D:/Other Projects/memes/scrappy/imgflip_scraper/dataset/templates'
            filename = '%s.json' % key
            complete_name = os.path.join(save_path, filename)
            with open(complete_name, 'w+') as file:
                url = meme['template_url']
                json.dump(meme, file, indent=2)
                # snapshot of the image in folder
                img_path = reduce(os.path.join, [save_path, "img", url.split('/')[-1]])
                self.log(meme)
                # r = requests.get(url, stream=True)
                # if r.status_code == 200:
                #     with open(img_path, 'wb') as f:
                #         r.raw.decode_content = True
                #         shutil.copyfileobj(r.raw, f)

                # resource = urllib.request.urlopen(meme['template_url'])
                # output = open(img_name, "wb")
                # output.write(resource.read())
                # output.close()
                # Fix from https://stackoverflow.com/questions/34957748/http-error-403-forbidden-with-urlretrieve
                opener = urllib.request.URLopener()
                opener.addheader('User-Agent', 'meme-crawler')
                opener.retrieve(url, img_path)
                # urllib.request.urlretrieve(url, img_path)
