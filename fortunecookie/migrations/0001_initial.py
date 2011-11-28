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

        # Adding model 'FortuneCookie'
        db.create_table('fortunecookie_fortunecookie', (
            ('basemodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['fortunecookie.BaseModel'], unique=True, primary_key=True)),
            ('fortune', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('chinese_word', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='fortune_cookies', null=True, blank=True, to=orm['fortunecookie.ChineseWord'])),
        ))
        db.send_create_signal('fortunecookie', ['FortuneCookie'])

        # Adding SortedM2M table for field lucky_numbers on 'FortuneCookie'
        db.create_table('fortunecookie_fortunecookie_lucky_numbers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('fortunecookie', models.ForeignKey(orm['fortunecookie.fortunecookie'], null=False)),
            ('luckynumber', models.ForeignKey(orm['fortunecookie.luckynumber'], null=False)),
            ('sort_value', models.IntegerField())
        ))
        db.create_unique('fortunecookie_fortunecookie_lucky_numbers', ['fortunecookie_id', 'luckynumber_id'])


    def backwards(self, orm):
        
        # Deleting model 'BaseModel'
        db.delete_table('fortunecookie_basemodel')

        # Deleting model 'LuckyNumber'
        db.delete_table('fortunecookie_luckynumber')

        # Deleting model 'ChineseWord'
        db.delete_table('fortunecookie_chineseword')

        # Deleting model 'FortuneCookie'
        db.delete_table('fortunecookie_fortunecookie')

        # Removing M2M table for field lucky_numbers on 'FortuneCookie'
        db.delete_table('fortunecookie_fortunecookie_lucky_numbers')


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
            'lucky_numbers': ('sortedm2m.fields.SortedManyToManyField', [], {'related_name': "'fortune_cookies'", 'symmetrical': 'False', 'to': "orm['fortunecookie.LuckyNumber']"})
        },
        'fortunecookie.luckynumber': {
            'Meta': {'ordering': "['number']", 'object_name': 'LuckyNumber', '_ormbases': ['fortunecookie.BaseModel']},
            'basemodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['fortunecookie.BaseModel']", 'unique': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['fortunecookie']
