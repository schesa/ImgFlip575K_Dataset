# :clown:ImgFlip575 Dataset

[About](#About) | [**Memes Dataset**](#memes-dataset) | [How to run](#how-to-run)

## About

Total memes - **575948**

Scraped top 100 popular memes from [Imgflip](https://imgflip.com/) using [Scrapy](https://docs.scrapy.org/en/latest/)

Used for **[generating memes using AI](https://github.com/schesa/ai-memes)**.

Can be used with [Imgflip API](https://api.imgflip.com/) to caption memes. This datast is a bigger version of [Imgflip top 24 memes](https://www.kaggle.com/dylanwenzlau/imgflip-meme-text-samples-for-top-24-memes).

## Memes Dataset

Top 100 popular memes ```./dataset/popular_100_memes.csv```

Nr of memes / template ```./dataset/statistics.json```

- Templates ```./dataset/templates```

Template Example
```yaml
{
  "title": "10 Guy Meme Template",
  "template_url": "https://imgflip.com/s/meme/10-Guy.jpg",
  "alternative_names": "Really High Guy, Stoner Stanley, Brainwashed Bob, stoned guy, ten guy, stoned buzzed high dude bro",
  "template_id": "101440",
  "format": "jpg",
  "dimensions": "500x454 px",
  "file_size": "24 KB"
}
```

- Memes ```./dataset/memes```
  
  Meme example:
```yaml
 {
    "url": "https://i.imgflip.com/2cpxta.jpg",
    "post": "https://imgflip.com/i/2cpxta",
    "metadata": {
      "views": "2,426",
      "img-votes": "4",
      "title": "Watch out or it'll eat you whole",
      "author": "PLarsen985"
    },
    "boxes": [
      "I USED TO CODE WITH PYTHON",
      "BUT I QUIT AFTER THE FIRST TIME IT BIT ME"
    ]
  }
```


## How to run
The dataset is already scraped in ./dataset

If you need fresh memes, just do:
```sh
$> cd project
```
```sh
$> pip install
```
```sh
$> run.sh 
```
