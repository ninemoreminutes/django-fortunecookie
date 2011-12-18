# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'ChineseWord', fields ['english_word', 'pinyin_word']
        db.create_unique('fortunecookie_chineseword', ['english_word', 'pinyin_word'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ChineseWord', fields ['english_word', 'pinyin_word']
        db.delete_unique('fortunecookie_chineseword', ['english_word', 'pinyin_word'])


    models = {
        'fortunecookie.chineseword': {
            'Meta': {'ordering': "['english_word']", 'unique_together': "(('english_word', 'pinyin_word'),)", 'object_name': 'ChineseWord'},
            'chinese_word': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'english_word': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pinyin_word': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'})
        },
        'fortunecookie.fortunecookie': {
            'Meta': {'ordering': "['fortune']", 'object_name': 'FortuneCookie'},
            'chinese_word': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'fortune_cookies'", 'null': 'True', 'blank': 'True', 'to': "orm['fortunecookie.ChineseWord']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fortune': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lucky_numbers': ('sortedm2m.fields.SortedManyToManyField', [], {'related_name': "'fortune_cookies'", 'symmetrical': 'False', 'to': "orm['fortunecookie.LuckyNumber']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'fortunecookie.luckynumber': {
            'Meta': {'ordering': "['number']", 'object_name': 'LuckyNumber'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['fortunecookie']
