from django.contrib import admin

from twits.models import Twit, Country, Word

admin.site.register(Twit)
admin.site.register(Country)
admin.site.register(Word)
