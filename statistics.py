from pathlib import Path
import json
import scrapy
import csv
import string
import os
from functools import reduce
import json
from os import listdir
from os.path import isfile, join
from collections import defaultdict

if __name__ == '__main__':
    memes = defaultdict(int)

    memes_path = reduce(os.path.join, [os.getcwd(), "dataset", 'memes'])
    files = (f for f in listdir(memes_path) if isfile(join(memes_path, f)))
    for file in files:
        file_path = reduce(os.path.join, [memes_path, file])
        with open(file_path) as json_file:
            data = json.load(json_file)
            memes[file] = len(data)
    statistics_path = reduce(os.path.join, [os.getcwd(), "dataset", 'statistics.json'])
    with open(statistics_path, 'w+') as result_file:
        json.dump({
            'total': reduce(lambda x, value: value + x, memes.values(), 0),
            'memes': memes
        }, result_file, indent=2)


