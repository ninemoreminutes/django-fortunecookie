# Django
from django.contrib import admin

# Django-FortuneCookie
from models import *

class LuckyNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'occurrences', 'created', 'modified')

class ChineseWordAdmin(admin.ModelAdmin):
    list_display = ('chinese_word', 'english_word', 'created', 'modified')

class LuckyNumberInline(admin.TabularInline):
    model = FortuneCookieLuckyNumber
    extra = 1
    fk_name = 'fortune_cookie'

class FortuneCookieAdmin(admin.ModelAdmin):
    list_display = ('fortune', 'chinese_word', 'lucky_numbers_display', 'created', 'modified')
    inlines = (LuckyNumberInline,)

admin.site.register(LuckyNumber, LuckyNumberAdmin)
admin.site.register(ChineseWord, ChineseWordAdmin)
admin.site.register(FortuneCookie, FortuneCookieAdmin)
