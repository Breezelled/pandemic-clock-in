from django.db import models


# Create your models here.

class Admin(models.Model):
    admin_id = models.CharField(max_length=255, blank=True, null=True)
    admin_name = models.CharField(max_length=255, blank=True, null=True)
    admin_org = models.CharField(max_length=255, blank=True, null=True, unique=True)
    admin_level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin'

    def __str__(self):
        return self.admin_name


class Org(models.Model):
    org_id = models.CharField(max_length=255, blank=True, null=True)
    org_name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    org_designate_location = models.CharField(max_length=255, blank=True, null=True)
    strategy_time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'org'

    def __str__(self):
        return self.org_name + " " + str(self.strategy_time)
