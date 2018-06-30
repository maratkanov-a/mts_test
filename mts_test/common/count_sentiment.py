import django
import os

from django.db.models import Sum

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mts_test.settings")
django.setup()

from twits.models import Twit, Word


def count_sentiment():
    for twit in Twit.objects.all():
        sentiment = Word.objects.filter(word__in=twit.tweet_text.split()).aggregate(Sum('value'))['value__sum']
        if sentiment:
            twit.tweet_sentiment = sentiment
            twit.save()
            print('sentiment for twit {} is calculated'.format(twit.id))


if __name__ == '__main__':
    count_sentiment()
