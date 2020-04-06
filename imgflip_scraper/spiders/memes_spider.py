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
                    # self.log('%s %s %s' % (row[0], row[1], row[2]))
                    url = 'https://imgflip.com/memetemplate/'
                    # delete punctuations
                    table = str.maketrans(dict.fromkeys(string.punctuation))
                    title = row[1].translate(table)
                    yield 'https://imgflip.com/memetemplate/' + "-".join(title.split())  # join words with -

    def start_requests(self):
        # urls = [
        #     'https://imgflip.com/memetemplate/Distracted-Boyfriend',
        # ]
        for url in self.get_urls():
            # self.log('scraping URL:%s' % url)
            yield scrapy.Request(url=url, callback=self.parse)

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

        # TODO get list of bounding boxes from /memegenerator/
        #  -> #mm-preview drag-box reverse order -> style x:left y:top width, height
        #  -> #mm-font-options color-btn font & outline style

        page = response.url.split("/")[-1]
        filename = '%s.json' % page
        save_path = 'D:/Other Projects/memes/scrappy/imgflip_scraper/dataset/templates'
        complete_name = os.path.join(save_path, filename)
        with open(complete_name, 'w+') as file:
            template_url = 'https://imgflip.com' + response.css('#mtm-img::attr(src)').get()
            meme = {
                'template_url': template_url,
                'alternative_names': alternative_names,
                'template_id': mtm_info[0],
                'format': mtm_info[1],
                'dimensions': mtm_info[2],
                'file_size': mtm_info[3]
            }
            # self.log('meme object %s' % meme)
            json.dump(meme, file, indent=2)
        # self.log('Created File %s' % filename)
        # yield meme
