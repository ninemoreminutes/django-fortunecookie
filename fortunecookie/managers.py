# Django
from django.db import models


class LuckyNumberManager(models.Manager):
    """Manager for the lucky number model."""

    def get_by_natural_key(self, number):
        return self.get(number=number)


class ChineseWordManager(models.Manager):
    """Manager for the Chinese word model."""

    def get_by_natural_key(self, english_word, pinyin_word):
        return self.get(english_word=english_word, pinyin_word=pinyin_word)
