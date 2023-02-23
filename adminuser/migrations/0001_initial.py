# Generated by Django 3.2.13 on 2022-05-08 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_id', models.CharField(blank=True, max_length=255, null=True)),
                ('admin_name', models.CharField(blank=True, max_length=255, null=True)),
                ('admin_org', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('admin_level', models.IntegerField(blank=True, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'adminuser',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_id', models.CharField(blank=True, max_length=255, null=True)),
                ('org_name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('org_designate_location', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'org',
                'managed': False,
            },
        ),
    ]