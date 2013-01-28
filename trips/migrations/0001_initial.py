# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Trip'
        db.create_table(u'trips_trip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('departure_city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('departure_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('destination_city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('destination_dt', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'trips', ['Trip'])


    def backwards(self, orm):
        # Deleting model 'Trip'
        db.delete_table(u'trips_trip')


    models = {
        u'trips.trip': {
            'Meta': {'object_name': 'Trip'},
            'departure_city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'departure_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'destination_city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'destination_dt': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['trips']