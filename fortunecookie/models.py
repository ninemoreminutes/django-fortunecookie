# Django
from django.db import models

class BaseModel(models.Model):
    """Base model class to track created and modified timestamps."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class LuckyNumber(BaseModel):
    """Unique lucky numbers from the fortune cookies."""

    class Meta:
        ordering = ['number']

    number = models.IntegerField(
        primary_key=True,
        help_text='The lucky number.'
    )

    def __unicode__(self):
        return u'%d' % self.number

    def occurrences(self):
        return self.fortune_cookies.count()

class ChineseWord(BaseModel):
    """English and Chinese translations of the 'Learn Chinese' word."""

    class Meta:
        ordering = ['english_word']

    english_word = models.CharField(
        max_length=64,
        help_text='English version of the word.'
    )
    pinyin_word = models.CharField(
        max_length=64,
        blank=True,
        default='',
        help_text='Hanyu Pinyin representation of the word.'
    )
    chinese_word = models.CharField(
        max_length=64,
        blank=True,
        default='',
        help_text='Simplified Chinese representation of the word.'
    )

    def __unicode__(self):
        return u'%s == %s' % (self.english_word, self.pinyin_word or '?')

    def occurrences(self):
        return self.fortune_cookies.count()

class FortuneCookieLuckyNumber(BaseModel):
    """Through table for relation between fortune cookies and lucky numbers."""

    class Meta:
        unique_together = ('fortune_cookie', 'lucky_number')
        order_with_respect_to = 'fortune_cookie'
        ordering = ['order', 'lucky_number']

    fortune_cookie = models.ForeignKey(
        'FortuneCookie',
        related_name='fortune_cookie_lucky_numbers'
    )
    lucky_number = models.ForeignKey(
        'LuckyNumber',
        related_name='fortune_cookie_lucky_numbers'
    )
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.lucky_number)

class FortuneCookie(BaseModel):
    """Fortune cookie: 29 cents; what a bargain!"""

    class Meta:
        ordering = ['fortune']

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
    lucky_numbers_display.short_description = 'Lucky numbers'

    def __unicode__(self):
        if self.lucky_numbers.count():
            return u'%s (%s)' % (self.fortune, self.lucky_numbers_display())
        else:
            return self.fortune
