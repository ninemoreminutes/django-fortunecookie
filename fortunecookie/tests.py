# Django
from django.test import TestCase

# Django-FortuneCookie
from fortunecookie.models import *

class TestFortuneCookie(TestCase):
    """Test cases for Django-FortuneCookie app."""

    def test_lucky_number(self):
        self.assertEqual(LuckyNumber.objects.count(), 0)
        ln1, created = LuckyNumber.objects.get_or_create(number=99)
        self.assertTrue(created)
        self.assertEqual(LuckyNumber.objects.count(), 1)
        self.assertEqual(ln1.number, 99)
        self.assertEqual(ln1.pk, 99)
        ln2, created = LuckyNumber.objects.get_or_create(number=99)
        self.assertFalse(created)
        self.assertEqual(ln2.pk, ln1.pk)
        ln3, created = LuckyNumber.objects.get_or_create(number=11)
        self.assertTrue(created)
        self.assertEqual(LuckyNumber.objects.count(), 2)
        self.assertEqual(ln3.number, 11)
        self.assertEqual(ln3.pk, 11)

    def test_chinese_word(self):
        self.assertEqual(ChineseWord.objects.count(), 0)
        cw1, created = ChineseWord.objects.get_or_create(english_word='dog')
        self.assertTrue(created)
        self.assertEqual(ChineseWord.objects.count(), 1)
        self.assertEqual(cw1.english_word, 'dog')
        self.assertEqual(cw1.pinyin_word, '')
        self.assertEqual(cw1.chinese_word, '')
        cw2, created = ChineseWord.objects.get_or_create(english_word='dog')
        self.assertFalse(created)
        self.assertEqual(cw2.pk, cw1.pk)
        cw3, created = ChineseWord.objects.get_or_create(english_word='cat')
        self.assertTrue(created)
        self.assertEqual(ChineseWord.objects.count(), 2)
        self.assertEqual(cw3.english_word, 'cat')
        self.assertEqual(cw3.pinyin_word, '')
        self.assertEqual(cw3.chinese_word, '')

    def test_fortune_cookie(self):
        self.assertEqual(FortuneCookie.objects.count(), 0)
        fc1, created = FortuneCookie.objects.get_or_create(fortune='test')
        self.assertTrue(created)
        self.assertEqual(fc1.fortune, 'test')
        self.assertEqual(fc1.chinese_word, None)
        self.assertEqual(fc1.lucky_numbers.count(), 0)
        
        #fc2 = FortuneCookie.objects.create(fortune='test', lucky_numbers=(3,5,7))
        #fc2a = FortuneCookie.objects.get(pk=fc2.pk)

    def test_protected_deletes(self):
        pass

    def test_fixture(self):
        pass
