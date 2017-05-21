# Py.Test
import pytest


@pytest.fixture
def apps(request, db):
    from django.apps import apps
    return apps


@pytest.fixture
def lucky_number_model(apps):
    return apps.get_model('fortunecookie', 'LuckyNumber')


@pytest.fixture
def chinese_word_model(apps):
    return apps.get_model('fortunecookie', 'ChineseWord')


@pytest.fixture
def fortune_cookie_model(apps):
    return apps.get_model('fortunecookie', 'FortuneCookie')


@pytest.fixture
def default_fortune_cookies(db):
    from django.core.management import call_command
    call_command('loaddata', 'fortunecookies.json')
