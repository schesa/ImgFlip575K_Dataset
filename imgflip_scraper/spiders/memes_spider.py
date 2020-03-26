import json
import scrapy


class MemesSpider(scrapy.Spider):
    name = "memes"

    def start_requests(self):
        # TODO get top 100 memes from https://api.imgflip.com/popular_meme_ids
        urls = [
            'https://imgflip.com/memetemplate/Distracted-Boyfriend',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ TODO
             get img with <img with id='mtm-mg'
             get Template ID, dimensions, file size, format
        """

        # TODO get list of bounding boxes from /memegenerator/
        #
        page = response.url.split("/")[-1]
        filename = '%s.json' % page
        with open(filename, 'w+') as file:
            meme = {'template': response.css('#mtm-img::attr(src)').get()}
            self.log('meme object %s' % meme)
            json.dump(meme, file)
        self.log('Created File %s' % filename)
        yield meme
