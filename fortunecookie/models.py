# Django
from django.db import models

class BaseModel(models.Model):
    """Base model class to track created and modified timestamps."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class LuckyNumber(BaseModel):
    """Unique lucky numbers from fortune cookies."""

    number = models.IntegerField(primary_key=True)

    def __unicode__(self):
        return u'%d' % self.number

    def occurrences(self):
        return self.fortune_cookies.count()

class ChineseWord(BaseModel):
    """"""

    chinese_word = models.CharField(max_length=32, unique=True)
    english_word = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return u'%s == %s' % (self.chinese_word, self.english_word)

class FortuneCookieLuckyNumber(BaseModel):

    fortune_cookie = models.ForeignKey('FortuneCookie', related_name='fortune_cookie_lucky_numbers')
    lucky_number = models.ForeignKey('LuckyNumber')
    order = models.IntegerField(default=0)

class FortuneCookie(BaseModel):
    """Fortune cookie: 29 cents; what a bargain!"""

    fortune = models.CharField(
        max_length=255,
        help_text='Confucious say...'
    )
    chinese_word = models.ForeignKey(
        'ChineseWord',
        related_name='fortune_cookies',
        blank=True,
        null=True,
        default=None,
        help_text='Learn Chinese.'
    )
    lucky_numbers = models.ManyToManyField(
        'LuckyNumber',
        through='FortuneCookieLuckyNumber',
        related_name='fortune_cookies',
        help_text='Lucky numbers.'
    )

    def lucky_numbers_display(self):
        return u', '.join(map(unicode, self.lucky_numbers.all()))

    def __unicode__(self):
        if self.lucky_numbers.count():
            return u'%s (%s)' % (self.fortune, self.lucky_numbers_display())
        else:
            return self.fortune
