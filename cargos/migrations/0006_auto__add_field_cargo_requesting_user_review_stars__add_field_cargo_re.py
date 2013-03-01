# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cargo.requesting_user_review_stars'
        db.add_column(u'cargos_cargo', 'requesting_user_review_stars',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Cargo.requesting_user_review_comment'
        db.add_column(u'cargos_cargo', 'requesting_user_review_comment',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Cargo.traveller_user_review_stars'
        db.add_column(u'cargos_cargo', 'traveller_user_review_stars',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Cargo.traveller_user_review_comment'
        db.add_column(u'cargos_cargo', 'traveller_user_review_comment',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Cargo.requesting_user_review_stars'
        db.delete_column(u'cargos_cargo', 'requesting_user_review_stars')

        # Deleting field 'Cargo.requesting_user_review_comment'
        db.delete_column(u'cargos_cargo', 'requesting_user_review_comment')

        # Deleting field 'Cargo.traveller_user_review_stars'
        db.delete_column(u'cargos_cargo', 'traveller_user_review_stars')

        # Deleting field 'Cargo.traveller_user_review_comment'
        db.delete_column(u'cargos_cargo', 'traveller_user_review_comment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cargos.cargo': {
            'Meta': {'object_name': 'Cargo'},
            'baggage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'books': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clothes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delivery': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'documents': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'duty_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'electronics': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'food': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medicaments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'others': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'personal_belongings': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pickup': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'requesting_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'my_cargos'", 'to': u"orm['auth.User']"}),
            'requesting_user_review_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'requesting_user_review_stars': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'traveller_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requested_cargos'", 'to': u"orm['auth.User']"}),
            'traveller_user_review_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'traveller_user_review_stars': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trips.Trip']"})
        },
        u'cargos.cargocomment': {
            'Meta': {'object_name': 'CargoComment'},
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cargos.Cargo']"}),
            'comment_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'creation_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'trips.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'trips.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'trips.trip': {
            'Meta': {'object_name': 'Trip'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creation_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dep_city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dep_city_trips'", 'null': 'True', 'to': u"orm['trips.City']"}),
            'dep_country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dep_country_trips'", 'null': 'True', 'to': u"orm['trips.Country']"}),
            'departure_city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'departure_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'dest_city': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dest_city_trips'", 'null': 'True', 'to': u"orm['trips.City']"}),
            'dest_country': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dest_country_trips'", 'null': 'True', 'to': u"orm['trips.Country']"}),
            'destination_city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'destination_dt': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'travelling_by': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['cargos']