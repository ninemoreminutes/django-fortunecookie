# Django
from django.contrib import admin

# Django-FortuneCookie
from models import *


class LuckyNumberAdmin(admin.ModelAdmin):
    """Admin configuration for lucky numbers."""

    list_display = ('number', 'occurrences', 'created', 'modified')


class ChineseWordAdmin(admin.ModelAdmin):
    """Admin configuration for Chinese words."""

    list_display = ('english_word', 'pinyin_word', 'chinese_word',
                    'occurrences', 'created', 'modified')


class FortuneCookieAdmin(admin.ModelAdmin):
    """Admin configuration for fortune cookies."""

    list_display = ('fortune', 'chinese_word', 'lucky_numbers_display',
                    'created', 'modified')
    list_select_related = True


admin.site.register(LuckyNumber, LuckyNumberAdmin)
admin.site.register(ChineseWord, ChineseWordAdmin)
admin.site.register(FortuneCookie, FortuneCookieAdmin)
