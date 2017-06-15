# Python
import sys

# Six
import six

# Django
from django.core.management import call_command
from django.db import models
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

# Py.Test
import pytest


def test_lucky_numbers(lucky_number_model):
    assert lucky_number_model.objects.count() == 0
    ln1, created = lucky_number_model.objects.get_or_create(number=99)
    assert created
    assert lucky_number_model.objects.count() == 1
    assert ln1.number == 99
    assert ln1.pk == 99
    assert six.text_type(ln1) == '99'
    assert int(ln1) == 99
    assert ln1.occurrences == 0
    ln2, created = lucky_number_model.objects.get_or_create(number=99)
    assert not created
    assert ln2.pk == ln1.pk
    ln3, created = lucky_number_model.objects.get_or_create(number=11)
    assert created
    assert lucky_number_model.objects.count() == 2
    assert ln3.number == 11
    assert ln3.pk == 11


def test_chinese_words(chinese_word_model):
    assert chinese_word_model.objects.count() == 0
    cw1, created = chinese_word_model.objects.get_or_create(english_word='dog')
    assert created
    assert chinese_word_model.objects.count() == 1
    assert cw1.english_word == 'dog'
    assert cw1.pinyin_word == ''
    assert cw1.chinese_word == ''
    assert six.text_type(cw1) == u'dog: ?'
    assert cw1.occurrences == 0
    cw2, created = chinese_word_model.objects.get_or_create(english_word='dog')
    assert not created
    assert cw2.pk == cw1.pk
    cw3, created = chinese_word_model.objects.get_or_create(english_word='cat', pinyin_word=u'M\u0101o', chinese_word=u'\u732b')
    assert created
    assert chinese_word_model.objects.count() == 2
    assert cw3.english_word == 'cat'
    assert cw3.pinyin_word == u'M\u0101o'
    assert cw3.chinese_word == u'\u732b'
    assert six.text_type(cw3) == u'cat: \u732b (M\u0101o)'
    cw4, created = chinese_word_model.objects.get_or_create(english_word='fish', chinese_word=u'\u9c7c')
    assert created
    assert chinese_word_model.objects.count() == 3
    assert cw4.english_word == 'fish'
    assert cw4.pinyin_word == ''
    assert cw4.chinese_word == u'\u9c7c'
    assert six.text_type(cw4) == u'fish: \u9c7c'


def test_fortune_cookies(lucky_number_model, chinese_word_model, fortune_cookie_model):
    ln1 = lucky_number_model.objects.create(number=95)
    ln2 = lucky_number_model.objects.create(number=32)
    assert fortune_cookie_model.objects.count() == 0
    fc1 = fortune_cookie_model.objects.create(fortune='test')
    assert fc1.fortune, 'test'
    assert fc1.chinese_word is None
    assert fc1.lucky_numbers.count() == 0
    assert six.text_type(fc1) == u'test'
    fc1.lucky_numbers.add(ln1)
    assert fc1.lucky_numbers.count() == 1
    assert fc1.lucky_numbers.all()[0].number == ln1.number
    fc1.lucky_numbers.add(ln2)
    assert fc1.lucky_numbers.count() == 2
    assert fc1.lucky_numbers.all()[0].number == ln1.number
    assert fc1.lucky_numbers.all()[1].number == ln2.number
    fc2 = fortune_cookie_model.objects.create(fortune='test', lucky_numbers=(3, 5, 7))
    assert fc2.pk != fc1.pk
    assert fc2.fortune == 'test'
    assert fc2.chinese_word is None
    assert fc2.lucky_numbers.count() == 3
    assert six.text_type(fc2) == u'test (3, 5, 7)'
    assert [x.number for x in fc2.lucky_numbers.all()] == [3, 5, 7]
    fc2.lucky_numbers.remove(5)
    assert [x.number for x in fc2.lucky_numbers.all()] == [3, 7]
    fc2.lucky_numbers.add(ln2)
    assert [x.number for x in fc2.lucky_numbers.all()] == [3, 7, 32]
    fc2.lucky_numbers.create(number=2)
    assert [x.number for x in fc2.lucky_numbers.all()] == [3, 7, 32, 2]
    fc2.lucky_numbers.clear()
    assert [x.number for x in fc2.lucky_numbers.all()] == []


def test_protected_delete(chinese_word_model, fortune_cookie_model):
    cw1 = chinese_word_model.objects.create(english_word='dog')
    fc1 = fortune_cookie_model.objects.create(fortune='test', chinese_word=cw1)
    assert fc1.chinese_word.pk == cw1.pk
    with pytest.raises(models.ProtectedError):
        cw1.delete()
    fc1.delete()
    assert chinese_word_model.objects.count() == 1
    cw1.delete()
    assert chinese_word_model.objects.count() == 0


def test_lucky_numbers_admin(admin_client, lucky_number_model, default_fortune_cookies):
    url = reverse('admin:fortunecookie_luckynumber_changelist')
    assert admin_client.get(url).status_code == 200
    url = '{}?fortune_cookies__count=0'.format(url)
    assert admin_client.get(url).status_code == 200
    lucky_number_data = lucky_number_model.objects.values('pk', 'number')[0]
    url = reverse('admin:fortunecookie_luckynumber_change', args=(lucky_number_data['pk'],))
    assert admin_client.get(url).status_code == 200
    assert admin_client.post(url, {'number': lucky_number_data['number']}, follow=True).status_code == 200
    url = reverse('admin:fortunecookie_luckynumber_history', args=(lucky_number_data['pk'],))
    assert admin_client.get(url).status_code == 200
    url = reverse('admin:fortunecookie_luckynumber_delete', args=(lucky_number_data['pk'],))
    assert admin_client.get(url).status_code == 200
    assert admin_client.post(url, {'post': 'yes'}, follow=True).status_code == 200
    assert not lucky_number_model.objects.filter(pk=lucky_number_data['pk']).exists()
    url = reverse('admin:fortunecookie_luckynumber_add')
    assert admin_client.get(url).status_code == 200
    assert admin_client.post(url, {'number': 999}, follow=True).status_code == 200
    assert lucky_number_model.objects.filter(number=999).exists()


def test_chinese_words_admin(admin_client, chinese_word_model, fortune_cookie_model, default_fortune_cookies):
    fortune_cookie_model.objects.all().delete()  # So we don't run into the protected issue when testing delete.
    url = reverse('admin:fortunecookie_chineseword_changelist')
    assert admin_client.get(url).status_code == 200
    url = '{}?fortune_cookies__count=1'.format(url)
    assert admin_client.get(url).status_code == 200
    chinese_word_data = chinese_word_model.objects.values('pk', 'english_word', 'pinyin_word', 'chinese_word')[0]
    url = reverse('admin:fortunecookie_chineseword_change', args=(chinese_word_data['pk'],))
    assert admin_client.get(url).status_code == 200
    updated_chinese_word_data = dict(chinese_word_data.items())
    updated_chinese_word_data['english_word'] = 'changed'
    assert admin_client.post(url, updated_chinese_word_data, follow=True).status_code == 200
    assert chinese_word_model.objects.get(pk=chinese_word_data['pk']).english_word == 'changed'
    url = reverse('admin:fortunecookie_chineseword_history', args=(chinese_word_data['pk'],))
    assert admin_client.get(url).status_code == 200
    url = reverse('admin:fortunecookie_chineseword_delete', args=(chinese_word_data['pk'],))
    assert admin_client.get(url).status_code == 200
    assert admin_client.post(url, {'post': 'yes'}, follow=True).status_code == 200
    assert not chinese_word_model.objects.filter(pk=chinese_word_data['pk']).exists()
    assert not chinese_word_model.objects.filter(english_word='changed').exists()
    url = reverse('admin:fortunecookie_chineseword_add')
    assert admin_client.get(url).status_code == 200
    assert admin_client.post(url, chinese_word_data, follow=True).status_code == 200
    assert chinese_word_model.objects.filter(english_word=chinese_word_data['english_word']).exists()


def test_fortune_cookies_admin(admin_client, chinese_word_model, fortune_cookie_model, default_fortune_cookies):
    fortune_cookie_model.objects.filter(chinese_word__isnull=True).first().lucky_numbers.clear()
    url = reverse('admin:fortunecookie_fortunecookie_changelist')
    assert admin_client.get(url).status_code == 200
    lucky_number = fortune_cookie_model.objects.filter(lucky_numbers__pk__isnull=False).first().lucky_numbers.first().pk
    url = '{}?lucky_numbers__number={}'.format(url, lucky_number)
    assert admin_client.get(url).status_code == 200
    fortune_cookie_data = fortune_cookie_model.objects.filter(chinese_word__isnull=False, lucky_numbers__pk__isnull=False).values('pk', 'fortune', 'chinese_word_id')[0]
    fortune_cookie_data['lucky_numbers'] = list(fortune_cookie_model.objects.get(pk=fortune_cookie_data['pk']).lucky_numbers.values_list('number', flat=True))
    url = reverse('admin:fortunecookie_fortunecookie_change', args=(fortune_cookie_data['pk'],))
    assert admin_client.get(url).status_code == 200
    updated_fortune_cookie_data = dict(fortune_cookie_data.items())
    updated_fortune_cookie_data['fortune'] = 'changed'
    updated_fortune_cookie_data['chinese_word'] = chinese_word_model.objects.exclude(pk=fortune_cookie_data['chinese_word_id']).first().pk
    # FIXME: Change lucky numbers!
    assert admin_client.post(url, updated_fortune_cookie_data, follow=True).status_code == 200
    assert fortune_cookie_model.objects.get(pk=fortune_cookie_data['pk']).fortune == 'changed'
    assert fortune_cookie_model.objects.get(pk=fortune_cookie_data['pk']).chinese_word_id == updated_fortune_cookie_data['chinese_word']
    url = reverse('admin:fortunecookie_fortunecookie_history', args=(fortune_cookie_data['pk'],))
    assert admin_client.get(url).status_code == 200
    url = reverse('admin:fortunecookie_fortunecookie_delete', args=(fortune_cookie_data['pk'],))
    assert admin_client.get(url).status_code == 200
    assert admin_client.post(url, {'post': 'yes'}, follow=True).status_code == 200
    assert not fortune_cookie_model.objects.filter(pk=fortune_cookie_data['pk']).exists()
    assert not fortune_cookie_model.objects.filter(fortune='changed').exists()
    url = reverse('admin:fortunecookie_fortunecookie_add')
    assert admin_client.get(url).status_code == 200
    assert admin_client.post(url, fortune_cookie_data, follow=True).status_code == 200
    assert fortune_cookie_model.objects.filter(fortune=fortune_cookie_data['fortune']).exists()


def test_fortunecookies_fixture(lucky_number_model, chinese_word_model, fortune_cookie_model, tmpdir):
    assert fortune_cookie_model.objects.count() == 0
    assert lucky_number_model.objects.count() == 0
    assert chinese_word_model.objects.count() == 0
    call_command('loaddata', 'fortunecookies.json')
    assert fortune_cookie_model.objects.count() == 13
    assert lucky_number_model.objects.count() == 99
    assert chinese_word_model.objects.count() == 6
    json_data = ''
    stdout = sys.stdout
    try:
        sys.stdout = six.StringIO()
        call_command('dumpdata', 'fortunecookie', natural_foreign=True)
        json_data = sys.stdout.getvalue()
    finally:
        sys.stdout = stdout
    assert json_data
    tmpfile = tmpdir.join('fctest.json')
    tmpfile.write_binary(six.binary_type(json_data.encode('utf8')))
    fortune_cookie_model.objects.all().delete()
    lucky_number_model.objects.all().delete()
    chinese_word_model.objects.all().delete()
    assert fortune_cookie_model.objects.count() == 0
    assert lucky_number_model.objects.count() == 0
    assert chinese_word_model.objects.count() == 0
    call_command('loaddata', tmpfile.strpath)
    assert fortune_cookie_model.objects.count() == 13
    assert lucky_number_model.objects.count() == 99
    assert chinese_word_model.objects.count() == 6
    call_command('loaddata', tmpfile.strpath)
    assert fortune_cookie_model.objects.count() == 13
    assert lucky_number_model.objects.count() == 99
    assert chinese_word_model.objects.count() == 6
