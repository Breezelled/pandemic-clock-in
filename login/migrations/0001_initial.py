# Generated by Django 4.0.3 on 2022-05-05 07:54

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(blank=True, max_length=255, null=True)),
                ('user_org', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('user_bind_num', models.CharField(blank=True, max_length=50, null=True)),
                ('profile_photo', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.IntegerField(blank=True, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('user_uuid', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_id', models.CharField(blank=True, max_length=255, null=True)),
                ('admin_name', models.CharField(blank=True, max_length=255, null=True)),
                ('admin_org', models.CharField(blank=True, max_length=255, null=True)),
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
