import json
import scrapy
import csv
import string
import os


class MemesSpider(scrapy.Spider):
    name = "memes"

    def get_urls(self):
        csv_filename = 'popular_100_memes.csv'
        with open(csv_filename) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            line = 0
            for row in reader:
                line += 1
                if line == 1:
                    self.log('HEADERS\n%s %s %s' % (row[0], row[1], row[2]))
                else:
                    self.log('%s %s %s' % (row[0], row[1], row[2]))
                    url = 'https://imgflip.com/memetemplate/'
                    # delete punctuations
                    table = str.maketrans(dict.fromkeys(string.punctuation))
                    title = row[1].translate(table)
                    yield 'https://imgflip.com/memetemplate/'+"-".join(title.split())  # join words with -

    def start_requests(self):
        # urls = [
        #     'https://imgflip.com/memetemplate/Distracted-Boyfriend',
        # ]
        for url in self.get_urls():
            self.log('scraping URL:%s' % url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ TODO
             get img with <img with id='mtm-mg'
             get Template ID, dimensions, file size, format
        """

        # TODO get list of bounding boxes from /memegenerator/

        page = response.url.split("/")[-1]
        filename = '%s.json' % page
        save_path = 'D:/Other Projects/memes/scrappy/imgflip_scraper/dataset/'
        complete_name = os.path.join(save_path, filename)
        with open(complete_name, 'w+') as file:
            meme = {'template': response.css('#mtm-img::attr(src)').get()}
            self.log('meme object %s' % meme)
            json.dump(meme, file)
        self.log('Created File %s' % filename)
        yield meme
