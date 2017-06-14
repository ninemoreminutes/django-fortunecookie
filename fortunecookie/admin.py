# Six
import six

# Django
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _
try:
    from django.urls import reverse
except ImportError:  # pragma: no cover
    from django.core.urlresolvers import reverse

# Django-FortuneCookie
from fortunecookie.models import LuckyNumber, ChineseWord, FortuneCookie


class OccurrencesListFilter(admin.SimpleListFilter):
    """Filter lists by number of occurrences in fortune cookies."""

    title = _('fortune cookie occurrences')
    parameter_name = 'fortune_cookies__count'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        occurrences = set(qs.values_list(self.parameter_name, flat=True))
        return [(x, six.text_type(x)) for x in sorted(occurrences)]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(fortune_cookies__count=self.value())


class LuckyNumberListFilter(admin.SimpleListFilter):
    """Filter fortune cookie list by lucky number."""

    title = _('lucky number')
    parameter_name = 'lucky_numbers__number'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        occurrences = set(qs.values_list('lucky_numbers__number', flat=True))
        return [(x, six.text_type(x)) for x in sorted(occurrences)]

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(lucky_numbers__number=self.value())


class OccurrencesMixin(object):
    """Mixin to annotate queries with count of fortune cookies."""

    def get_queryset(self, request):
        qs = super(OccurrencesMixin, self).get_queryset(request)
        return qs.annotate(Count('fortune_cookies'))

    def get_occurrences_display(self, obj=None):
        url = reverse('admin:fortunecookie_fortunecookie_changelist')
        return format_html('<a href="{}?{}={}">{}</a>', url,
                           self.occurrences_lookup, obj.pk, obj.occurrences)

    get_occurrences_display.short_description = _('Occurrences')
    get_occurrences_display.allow_tags = True
    get_occurrences_display.admin_order_field = 'fortune_cookies__count'


class LuckyNumberAdmin(OccurrencesMixin, admin.ModelAdmin):
    """Admin configuration for lucky numbers."""

    list_display = ('number', 'get_occurrences_display', 'created', 'modified')
    list_filter = (OccurrencesListFilter,)
    fields = ('number', 'get_occurrences_display', 'created', 'modified')
    readonly_fields = ('get_occurrences_display', 'created', 'modified')
    occurrences_lookup = 'lucky_numbers__number__exact'

    def get_fields(self, request, obj=None):
        return ('number',) if obj is None else self.fields

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj is None else self.fields


class ChineseWordAdmin(OccurrencesMixin, admin.ModelAdmin):
    """Admin configuration for Chinese words."""

    list_display = ('english_word', 'pinyin_word', 'chinese_word',
                    'get_occurrences_display', 'created', 'modified')
    list_filter = (OccurrencesListFilter,)
    fields = ('english_word', 'pinyin_word', 'chinese_word',
              'get_occurrences_display', 'created', 'modified')
    readonly_fields = ('get_occurrences_display', 'created', 'modified')
    occurrences_lookup = 'chinese_word__id__exact'


class FortuneCookieAdmin(admin.ModelAdmin):
    """Admin configuration for fortune cookies."""

    list_display = ('fortune', 'get_chinese_word_display',
                    'get_lucky_numbers_display', 'created', 'modified')
    list_filter = ('chinese_word', LuckyNumberListFilter)
    fields = ('fortune', 'chinese_word', 'lucky_numbers', 'created', 'modified')
    readonly_fields = ('created', 'modified')

    def get_queryset(self, request):
        qs = super(FortuneCookieAdmin, self).get_queryset(request)
        return qs.select_related('chinese_word').prefetch_related('lucky_numbers')

    def get_lucky_numbers_display(self, obj=None):
        if obj and obj.lucky_numbers.exists():
            return format_html_join(', ', u'<a href="{}">{}</a>', [
                (reverse('admin:fortunecookie_luckynumber_change', args=(ln.pk,)), ln)
                for ln in obj.lucky_numbers.all()
            ])
        return '-'

    get_lucky_numbers_display.short_description = _('Lucky numbers')
    get_lucky_numbers_display.allow_tags = True

    def get_chinese_word_display(self, obj=None):
        if obj and obj.chinese_word_id:
            url = reverse('admin:fortunecookie_chineseword_change',
                          args=(obj.chinese_word_id,))
            return format_html(u'<a href="{}">{}</a>', url, obj.chinese_word)
        return '-'

    get_chinese_word_display.short_description = _('Chinese word')
    get_chinese_word_display.allow_tags = True
    get_chinese_word_display.admin_order_field = 'chinese_word'


admin.site.register(LuckyNumber, LuckyNumberAdmin)
admin.site.register(ChineseWord, ChineseWordAdmin)
admin.site.register(FortuneCookie, FortuneCookieAdmin)
