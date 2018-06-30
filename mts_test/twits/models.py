from django.db import models
import pycountry
import datetime


class Twit(models.Model):
    name = models.CharField(max_length=100, null=True)
    tweet_text = models.TextField()
    display_url = models.TextField()
    created_at = models.DateTimeField()
    tweet_sentiment = models.IntegerField(default=0)
    country = models.ForeignKey('Country', on_delete=models.PROTECT)

    @classmethod
    def create(cls, data=None):
        if data is None:
            data = {}

        if 'delete' in data:
            return

        country_obj = Country.get_or_create({
            "location": data.get('user', {}).get('location'),
            "lang": data.get("lang")
        })

        name = data.get('user', {}).get('screen_name')
        display_url = 'https://twitter.com/{}/status/{}'.format(name, data.get('id'))
        created_at = datetime.datetime.fromtimestamp(int(data.get('timestamp_ms')) / 1000).strftime('%Y-%m-%d %H:%M:%S')

        cls(
            name=name,
            tweet_text=data.get('text'),
            created_at=created_at,
            display_url=display_url,
            country=country_obj
        ).save()


class Country(models.Model):
    location = models.TextField()
    lang = models.CharField(max_length=10)
    country_code = models.IntegerField(null=True)

    @classmethod
    def get_or_create(cls, data):
        lang = data.get('lang')

        country = cls.get_country(lang)

        country_obj, _ = Country.objects.get_or_create(
            lang=lang,
            location=getattr(country, 'name', data.get('location')),
            country_code=getattr(country, 'numeric', None)
        )

        return country_obj

    @classmethod
    def get_country(cls, lang):
        search_dict = {}
        if len(lang) == 2:
            search_dict["alpha_2"] = lang
        else:
            search_dict["alpha_3"] = lang
        try:
            pycountry.languages.get(**search_dict)

            return pycountry.countries.lookup(lang)
        except (LookupError, KeyError):
            return type('', (), {})()


class Word(models.Model):
    word = models.CharField(max_length=100)
    value = models.SmallIntegerField()

    @classmethod
    def create(cls, line):
        word, value = line.split('\t')
        return cls(word=word, value=value)
