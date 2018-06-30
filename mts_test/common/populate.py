import json

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mts_test.settings")
django.setup()

from twits.models import Twit, Word


def populate_words():
    with open('./files/AFINN-111.txt', 'r') as words_file:
        create_list = []
        for line in words_file:
            create_list.append(Word.create(line))
        Word.objects.bulk_create(create_list)


def populate_db():
    with open('./files/three_minutes_tweets.json.txt', 'r') as populate_file:
        for line in populate_file:
            line_dict = json.loads(line)
            Twit.create(line_dict)


if __name__ == '__main__':
    populate_words()
    populate_db()
