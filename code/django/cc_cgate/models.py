from django.db import models
from django_mysql.models import JSONField, Model

# Create your models here.

class QuoteItem(models.Model):
  id = models.AutoField(primary_key=True)
  quote_id = models.IntegerField()
  quote_bundle_id = models.IntegerField(blank=True, null=True)
  item_type = models.CharField(max_length=50, blank=True, null=True)
  loc_ref = models.IntegerField(blank=True, null=True)
  job_data = JSONField(blank=True, null=True)  # This field type is a guess.
  params_data = JSONField(blank=True, null=True)  # This field type is a guess.
  data_raw = JSONField(blank=True, null=True)  # This field type is a guess.
  data_proc = JSONField(blank=True, null=True)  # This field type is a guess.
  created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

  class Meta:
    managed = False
    db_table = 'quote_items'


class QuoteBundle(models.Model):
  id = models.AutoField(primary_key=True)
  quote_id = models.IntegerField(blank=True, null=True)
  params_data = JSONField(blank=True, null=True)  # This field type is a guess.
  created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

  class Meta:
    managed = False
    db_table = 'quote_bundles'


class Quote(models.Model):
  id = models.AutoField(primary_key=True)
  created_by = models.CharField(max_length=255, blank=True, null=True)
  customer_name = models.CharField(max_length=255, blank=True, null=True)
  description = models.CharField(max_length=255, blank=True, null=True)
  preferences_data = JSONField(blank=True, null=True)  # This field type is a guess.
  created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

  class Meta:
    managed = False
    db_table = 'quotes'


class TrackedEvent(models.Model):
  id = models.AutoField(primary_key=True)
  table_name = models.CharField(max_length=255, blank=True, null=True)
  table_id = models.IntegerField(blank=True, null=True)
  event_data = JSONField(blank=True, null=True)  # This field type is a guess.
  created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
  updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

  class Meta:
    managed = False
    db_table = 'tracked_events'