from django.db import models


# Create your models here.


class Area(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=20)
    citycode = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'area'


class City(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=20)
    provincecode = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'city'


class Org(models.Model):
    org_id = models.CharField(max_length=255, blank=True, null=True)
    org_name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    org_designate_location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'org'


class Province(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'province'


class Record(models.Model):
    record_id = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    ip = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    designate_location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'record'


class RecordInfo(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True)
    ill = models.IntegerField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    symptom = models.IntegerField(blank=True, null=True)
    symptom_list = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.IntegerField(blank=True, null=True)
    hospital_location = models.CharField(max_length=255, blank=True, null=True)
    medicine = models.IntegerField(blank=True, null=True)
    medicine_detail = models.CharField(max_length=255, blank=True, null=True)
    designate_location = models.IntegerField(blank=True, null=True)
    record_id = models.CharField(max_length=255, blank=True, null=True)
    live_type = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'record_info'
