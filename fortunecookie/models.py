# Django
from django.db import models

# Django-SortedM2M
from sortedm2m.fields import SortedManyToManyField


class BaseModel(models.Model):
    """Base model class to track created and modified timestamps."""

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class LuckyNumberManager(models.Manager):
    """Manager for the lucky number model."""

    def get_by_natural_key(self, number):
        return self.get(number=number)


class LuckyNumber(BaseModel):
    """Unique lucky numbers from the fortune cookies."""

    class Meta:
        ordering = ['number']

    objects = LuckyNumberManager()

    number = models.IntegerField(
        primary_key=True,
        help_text='The lucky number.'
    )

    def __unicode__(self):
        return u'%d' % self.number

    def __int__(self):
        return self.number

    def natural_key(self):
        return (self.number,)

    @property
    def occurrences(self):
        return self.fortune_cookies.count()


class ChineseWordManager(models.Manager):
    """Manager for the Chinese word model."""

    def get_by_natural_key(self, english_word, pinyin_word):
        return self.get(english_word=english_word, pinyin_word=pinyin_word)


class ChineseWord(BaseModel):
    """English and Chinese translations of the 'Learn Chinese' word."""

    class Meta:
        unique_together = ('english_word', 'pinyin_word')
        ordering = ['english_word']

    objects = ChineseWordManager()

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
        if self.pinyin_word and self.chinese_word:
            return u'%s: %s (%s)' % (self.english_word, self.chinese_word,
                                     self.pinyin_word)
        elif self.chinese_word:
            return u'%s: %s' % (self.english_word, self.chinese_word)
        else:
            return u'%s: %s' % (self.english_word, self.pinyin_word or '?')

    def natural_key(self):
        return (self.english_word, self.pinyin_word)

    @property
    def occurrences(self):
        return self.fortune_cookies.count()


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
        on_delete=models.PROTECT,
        help_text='Learn Chinese.'
    )
    lucky_numbers = SortedManyToManyField(
        'LuckyNumber',
        related_name='fortune_cookies',
        help_text='Lucky numbers.'
    )

    def __init__(self, *args, **kwargs):
        self._init_lucky_numbers = kwargs.pop('lucky_numbers', None)
        super(FortuneCookie, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        #if isinstance(self.chinese_word, basestring):
        #    self.chinese_word = \
        #   ChineseWord.objects.get_or_create(english_word=self.chinese_word)
        #elif isinstance(self.chinese_word, (tuple, list)) and \
        #        len(self.chinese_word):
        #    d = dict(zip(['english_word', 'pinyin_word', 'chinese_word'],
        #             self.chinese_word))
        #    self.chinese_word = ChineseWord.objects.get_or_create(**d)
        if not self.pk and self._init_lucky_numbers and \
                isinstance(self._init_lucky_numbers, (list, tuple)):
            lucky_numbers = self._init_lucky_numbers
        else:
            lucky_numbers = []
        super(FortuneCookie, self).save(*args, **kwargs)
        for number in lucky_numbers:
            ln = LuckyNumber.objects.get_or_create(number=int(number))[0]
            self.lucky_numbers.add(ln)

    def lucky_numbers_display(self):
        return u', '.join(map(unicode, self.lucky_numbers.all()))
    lucky_numbers_display.short_description = 'Lucky numbers'

    def __unicode__(self):
        if self.lucky_numbers.count():
            return u'%s (%s)' % (self.fortune, self.lucky_numbers_display())
        else:
            return self.fortune
