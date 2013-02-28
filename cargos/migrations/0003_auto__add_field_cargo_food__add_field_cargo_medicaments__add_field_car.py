# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cargo.food'
        db.add_column(u'cargos_cargo', 'food',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cargo.medicaments'
        db.add_column(u'cargos_cargo', 'medicaments',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cargo.duty_free'
        db.add_column(u'cargos_cargo', 'duty_free',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cargo.electronics'
        db.add_column(u'cargos_cargo', 'electronics',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cargo.baggage'
        db.add_column(u'cargos_cargo', 'baggage',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cargo.books'
        db.add_column(u'cargos_cargo', 'books',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cargo.documents'
        db.add_column(u'cargos_cargo', 'documents',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cargo.personal_belongings'
        db.add_column(u'cargos_cargo', 'personal_belongings',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cargo.clothes'
        db.add_column(u'cargos_cargo', 'clothes',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Cargo.others'
        db.add_column(u'cargos_cargo', 'others',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Cargo.price'
        db.add_column(u'cargos_cargo', 'price',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Cargo.pickup'
        db.add_column(u'cargos_cargo', 'pickup',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Cargo.delivery'
        db.add_column(u'cargos_cargo', 'delivery',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Cargo.food'
        db.delete_column(u'cargos_cargo', 'food')

        # Deleting field 'Cargo.medicaments'
        db.delete_column(u'cargos_cargo', 'medicaments')

        # Deleting field 'Cargo.duty_free'
        db.delete_column(u'cargos_cargo', 'duty_free')

        # Deleting field 'Cargo.electronics'
        db.delete_column(u'cargos_cargo', 'electronics')

        # Deleting field 'Cargo.baggage'
        db.delete_column(u'cargos_cargo', 'baggage')

        # Deleting field 'Cargo.books'
        db.delete_column(u'cargos_cargo', 'books')

        # Deleting field 'Cargo.documents'
        db.delete_column(u'cargos_cargo', 'documents')

        # Deleting field 'Cargo.personal_belongings'
        db.delete_column(u'cargos_cargo', 'personal_belongings')

        # Deleting field 'Cargo.clothes'
        db.delete_column(u'cargos_cargo', 'clothes')

        # Deleting field 'Cargo.others'
        db.delete_column(u'cargos_cargo', 'others')

        # Deleting field 'Cargo.price'
        db.delete_column(u'cargos_cargo', 'price')

        # Deleting field 'Cargo.pickup'
        db.delete_column(u'cargos_cargo', 'pickup')

        # Deleting field 'Cargo.delivery'
        db.delete_column(u'cargos_cargo', 'delivery')


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
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'traveller_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requested_cargos'", 'to': u"orm['auth.User']"}),
            'trip': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trips.Trip']"})
        },
        u'cargos.cargocomment': {
            'Meta': {'object_name': 'CargoComment'},
            'cargo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cargos.Cargo']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
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