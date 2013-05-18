# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Country'
        db.delete_table(u'trips_country')

        # Deleting model 'City'
        db.delete_table(u'trips_city')

        # Deleting field 'Trip.dest_city'
        db.delete_column(u'trips_trip', 'dest_city_id')

        # Deleting field 'Trip.dest_country'
        db.delete_column(u'trips_trip', 'dest_country_id')

        # Deleting field 'Trip.departure_dt'
        db.delete_column(u'trips_trip', 'departure_dt')

        # Deleting field 'Trip.departure_city'
        db.delete_column(u'trips_trip', 'departure_city')

        # Deleting field 'Trip.dep_city'
        db.delete_column(u'trips_trip', 'dep_city_id')

        # Deleting field 'Trip.destination_city'
        db.delete_column(u'trips_trip', 'destination_city')

        # Deleting field 'Trip.destination_dt'
        db.delete_column(u'trips_trip', 'destination_dt')

        # Deleting field 'Trip.dep_country'
        db.delete_column(u'trips_trip', 'dep_country_id')


    def backwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'trips_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'trips', ['Country'])

        # Adding model 'City'
        db.create_table(u'trips_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'trips', ['City'])

        # Adding field 'Trip.dest_city'
        db.add_column(u'trips_trip', 'dest_city',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='dest_city_trips', null=True, to=orm['trips.City'], blank=True),
                      keep_default=False)

        # Adding field 'Trip.dest_country'
        db.add_column(u'trips_trip', 'dest_country',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='dest_country_trips', null=True, to=orm['trips.Country'], blank=True),
                      keep_default=False)

        # Adding field 'Trip.departure_dt'
        db.add_column(u'trips_trip', 'departure_dt',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Trip.departure_city'
        raise RuntimeError("Cannot reverse this migration. 'Trip.departure_city' and its values cannot be restored.")
        # Adding field 'Trip.dep_city'
        db.add_column(u'trips_trip', 'dep_city',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='dep_city_trips', null=True, to=orm['trips.City'], blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Trip.destination_city'
        raise RuntimeError("Cannot reverse this migration. 'Trip.destination_city' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Trip.destination_dt'
        raise RuntimeError("Cannot reverse this migration. 'Trip.destination_dt' and its values cannot be restored.")
        # Adding field 'Trip.dep_country'
        db.add_column(u'trips_trip', 'dep_country',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='dep_country_trips', null=True, to=orm['trips.Country'], blank=True),
                      keep_default=False)


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'trips.trip': {
            'Meta': {'object_name': 'Trip'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creation_dt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'travelling_by': ('django.db.models.fields.IntegerField', [], {}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['trips']