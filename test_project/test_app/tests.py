# Python
import sys
import tempfile

# Six
import six

# Django
from django.test import TestCase
from django.core.management import call_command
from django.db import models

# Django-FortuneCookie
from fortunecookie.models import LuckyNumber, ChineseWord, FortuneCookie


class TestFortuneCookie(TestCase):
    """Test cases for Django-FortuneCookie app."""

    def test_lucky_number(self):
        self.assertEqual(LuckyNumber.objects.count(), 0)
        ln1, created = LuckyNumber.objects.get_or_create(number=99)
        self.assertTrue(created)
        self.assertEqual(LuckyNumber.objects.count(), 1)
        self.assertEqual(ln1.number, 99)
        self.assertEqual(ln1.pk, 99)
        self.assertEqual(six.text_type(ln1), '99')
        self.assertEqual(int(ln1), 99)
        self.assertEqual(ln1.occurrences, 0)
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
        self.assertEqual(six.text_type(cw1), u'dog: ?')
        self.assertEqual(cw1.occurrences, 0)
        cw2, created = ChineseWord.objects.get_or_create(english_word='dog')
        self.assertFalse(created)
        self.assertEqual(cw2.pk, cw1.pk)
        cw3, created = ChineseWord.objects.get_or_create(english_word='cat', pinyin_word=u'M\u0101o', chinese_word=u'\u732b')
        self.assertTrue(created)
        self.assertEqual(ChineseWord.objects.count(), 2)
        self.assertEqual(cw3.english_word, 'cat')
        self.assertEqual(cw3.pinyin_word, u'M\u0101o')
        self.assertEqual(cw3.chinese_word, u'\u732b')
        self.assertEqual(six.text_type(cw3), u'cat: \u732b (M\u0101o)')
        cw4, created = ChineseWord.objects.get_or_create(english_word='fish', chinese_word=u'\u9c7c')
        self.assertTrue(created)
        self.assertEqual(ChineseWord.objects.count(), 3)
        self.assertEqual(cw4.english_word, 'fish')
        self.assertEqual(cw4.pinyin_word, '')
        self.assertEqual(cw4.chinese_word, u'\u9c7c')
        self.assertEqual(six.text_type(cw4), u'fish: \u9c7c')

    def test_fortune_cookie(self):
        ln1 = LuckyNumber.objects.create(number=95)
        ln2 = LuckyNumber.objects.create(number=32)
        self.assertEqual(FortuneCookie.objects.count(), 0)
        fc1 = FortuneCookie.objects.create(fortune='test')
        self.assertEqual(fc1.fortune, 'test')
        self.assertEqual(fc1.chinese_word, None)
        self.assertEqual(fc1.lucky_numbers.count(), 0)
        self.assertEqual(six.text_type(fc1), u'test')
        fc1.lucky_numbers.add(ln1)
        self.assertEqual(fc1.lucky_numbers.count(), 1)
        self.assertEqual(fc1.lucky_numbers.all()[0].number, ln1.number)
        fc1.lucky_numbers.add(ln2)
        self.assertEqual(fc1.lucky_numbers.count(), 2)
        self.assertEqual(fc1.lucky_numbers.all()[0].number, ln1.number)
        self.assertEqual(fc1.lucky_numbers.all()[1].number, ln2.number)
        fc2 = FortuneCookie.objects.create(fortune='test',
                                           lucky_numbers=(3, 5, 7))
        self.assertNotEqual(fc2.pk, fc1.pk)
        self.assertEqual(fc2.fortune, 'test')
        self.assertEqual(fc2.chinese_word, None)
        self.assertEqual(fc2.lucky_numbers.count(), 3)
        self.assertEqual(six.text_type(fc2), u'test (3, 5, 7)')
        self.assertEqual([x.number for x in fc2.lucky_numbers.all()],
                         [3, 5, 7])
        fc2.lucky_numbers.remove(5)
        self.assertEqual([x.number for x in fc2.lucky_numbers.all()], [3, 7])
        fc2.lucky_numbers.add(ln2)
        self.assertEqual([x.number for x in fc2.lucky_numbers.all()],
                         [3, 7, 32])
        fc2.lucky_numbers.create(number=2)
        self.assertEqual([x.number for x in fc2.lucky_numbers.all()],
                         [3, 7, 32, 2])
        fc2.lucky_numbers.clear()
        self.assertEqual([x.number for x in fc2.lucky_numbers.all()], [])

    def test_protected_delete(self):
        cw1 = ChineseWord.objects.create(english_word='dog')
        fc1 = FortuneCookie.objects.create(fortune='test', chinese_word=cw1)
        self.assertEqual(fc1.chinese_word.pk, cw1.pk)
        self.assertRaises(models.ProtectedError, cw1.delete)
        fc1.delete()
        self.assertEqual(ChineseWord.objects.count(), 1)
        cw1.delete()
        self.assertEqual(ChineseWord.objects.count(), 0)

    def test_fixture(self):
        self.assertEqual(FortuneCookie.objects.count(), 0)
        self.assertEqual(LuckyNumber.objects.count(), 0)
        self.assertEqual(ChineseWord.objects.count(), 0)
        call_command('loaddata', 'fortunecookies.json')
        self.assertEqual(FortuneCookie.objects.count(), 13)
        self.assertEqual(LuckyNumber.objects.count(), 99)
        self.assertEqual(ChineseWord.objects.count(), 6)
        json_data = ''
        stdout = sys.stdout
        try:
            sys.stdout = six.StringIO()
            call_command('dumpdata', 'fortunecookie', natural_foreign=True)
            json_data = sys.stdout.getvalue()
        finally:
            sys.stdout = stdout
        self.assertTrue(json_data)
        tf = tempfile.NamedTemporaryFile(suffix='.json')
        json_data = json_data.encode('utf8')
        tf.write(six.binary_type(json_data))
        tf.flush()
        FortuneCookie.objects.all().delete()
        LuckyNumber.objects.all().delete()
        ChineseWord.objects.all().delete()
        self.assertEqual(FortuneCookie.objects.count(), 0)
        self.assertEqual(LuckyNumber.objects.count(), 0)
        self.assertEqual(ChineseWord.objects.count(), 0)
        call_command('loaddata', tf.name)
        self.assertEqual(FortuneCookie.objects.count(), 13)
        self.assertEqual(LuckyNumber.objects.count(), 99)
        self.assertEqual(ChineseWord.objects.count(), 6)
        call_command('loaddata', tf.name)
        self.assertEqual(FortuneCookie.objects.count(), 13)
        self.assertEqual(LuckyNumber.objects.count(), 99)
        self.assertEqual(ChineseWord.objects.count(), 6)
