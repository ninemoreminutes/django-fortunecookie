# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BaseModel'
        db.create_table('fortunecookie_basemodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('fortunecookie', ['BaseModel'])

        # Adding model 'LuckyNumber'
        db.create_table('fortunecookie_luckynumber', (
            ('basemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fortunecookie.BaseModel'], unique=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal('fortunecookie', ['LuckyNumber'])

        # Adding model 'ChineseWord'
        db.create_table('fortunecookie_chineseword', (
            ('basemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fortunecookie.BaseModel'], unique=True, primary_key=True)),
            ('english_word', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('pinyin_word', self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True)),
            ('chinese_word', self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True)),
        ))
        db.send_create_signal('fortunecookie', ['ChineseWord'])

        # Adding model 'FortuneCookieLuckyNumber'
        db.create_table('fortunecookie_fortunecookieluckynumber', (
            ('basemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fortunecookie.BaseModel'], unique=True, primary_key=True)),
            ('fortune_cookie', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fortune_cookie_lucky_numbers', to=orm['fortunecookie.FortuneCookie'])),
            ('lucky_number', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fortune_cookie_lucky_numbers', to=orm['fortunecookie.LuckyNumber'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('fortunecookie', ['FortuneCookieLuckyNumber'])

        # Adding unique constraint on 'FortuneCookieLuckyNumber', fields ['fortune_cookie', 'lucky_number']
        db.create_unique('fortunecookie_fortunecookieluckynumber', ['fortune_cookie_id', 'lucky_number_id'])

        # Adding model 'FortuneCookie'
        db.create_table('fortunecookie_fortunecookie', (
            ('basemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fortunecookie.BaseModel'], unique=True, primary_key=True)),
            ('fortune', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('chinese_word', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='fortune_cookies', null=True, blank=True, to=orm['fortunecookie.ChineseWord'])),
        ))
        db.send_create_signal('fortunecookie', ['FortuneCookie'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FortuneCookieLuckyNumber', fields ['fortune_cookie', 'lucky_number']
        db.delete_unique('fortunecookie_fortunecookieluckynumber', ['fortune_cookie_id', 'lucky_number_id'])

        # Deleting model 'BaseModel'
        db.delete_table('fortunecookie_basemodel')

        # Deleting model 'LuckyNumber'
        db.delete_table('fortunecookie_luckynumber')

        # Deleting model 'ChineseWord'
        db.delete_table('fortunecookie_chineseword')

        # Deleting model 'FortuneCookieLuckyNumber'
        db.delete_table('fortunecookie_fortunecookieluckynumber')

        # Deleting model 'FortuneCookie'
        db.delete_table('fortunecookie_fortunecookie')


    models = {
        'fortunecookie.basemodel': {
            'Meta': {'object_name': 'BaseModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'fortunecookie.chineseword': {
            'Meta': {'ordering': "['english_word']", 'object_name': 'ChineseWord', '_ormbases': ['fortunecookie.BaseModel']},
            'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fortunecookie.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'chinese_word': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'english_word': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pinyin_word': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'})
        },
        'fortunecookie.fortunecookie': {
            'Meta': {'ordering': "['fortune']", 'object_name': 'FortuneCookie', '_ormbases': ['fortunecookie.BaseModel']},
            'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fortunecookie.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'chinese_word': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'fortune_cookies'", 'null': 'True', 'blank': 'True', 'to': "orm['fortunecookie.ChineseWord']"}),
            'fortune': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'lucky_numbers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'fortune_cookies'", 'symmetrical': 'False', 'through': "orm['fortunecookie.FortuneCookieLuckyNumber']", 'to': "orm['fortunecookie.LuckyNumber']"})
        },
        'fortunecookie.fortunecookieluckynumber': {
            'Meta': {'ordering': "('_order',)", 'unique_together': "(('fortune_cookie', 'lucky_number'),)", 'object_name': 'FortuneCookieLuckyNumber', '_ormbases': ['fortunecookie.BaseModel']},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fortunecookie.BaseModel']", 'unique': 'True', 'primary_key': 'True'}),
            'fortune_cookie': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fortune_cookie_lucky_numbers'", 'to': "orm['fortunecookie.FortuneCookie']"}),
            'lucky_number': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fortune_cookie_lucky_numbers'", 'to': "orm['fortunecookie.LuckyNumber']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'fortunecookie.luckynumber': {
            'Meta': {'ordering': "['number']", 'object_name': 'LuckyNumber', '_ormbases': ['fortunecookie.BaseModel']},
            'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fortunecookie.BaseModel']", 'unique': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['fortunecookie']
