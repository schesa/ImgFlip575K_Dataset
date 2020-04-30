# About

A bigger version of **[Imgflip top 24 memes](https://www.kaggle.com/dylanwenzlau/imgflip-meme-text-samples-for-top-24-memes)**

Scraped top 100 popular memes from **[Imgflip](https://imgflip.com/)**

Total memes - **574701**

Can be used with **[Imgflip API](https://api.imgflip.com/)**

# Memes Dataset


Top 100 popular memes ```./dataset/popular_100_memes.csv```

- Templates ```./dataset/templates```

- Statistics ```./dataset/statistics.json```

- Memes ```./dataset/memes```
  example:
```json
{
    "url": "https://i.imgflip.com/3pxtz2.jpg",
    "post": "https://imgflip.com/i/3pxtz2",
    "metadata":
      "views": "1,335",
      "img-votes": "1,335",
      "title": "Yo Dawg Heard You",
      "author": "Trouble869"
    },
    "boxes": [
      "WHEN YOU'RE HAVING A BAD DAY",
      "BUT THEN YOU FIND OUT WHO YOUR EX IS DATING NOW"
    ]
  }
```


# How to run
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
