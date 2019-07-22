# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-22 11:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assignementdata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_start_time', models.DateTimeField()),
                ('assigned_end_time', models.DateTimeField()),
                ('event_id', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Availabledata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_start_time', models.DateTimeField()),
                ('available_end_time', models.DateTimeField()),
                ('event_id', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('token', models.CharField(blank=True, max_length=100, null=True)),
                ('refresh_token', models.CharField(blank=True, max_length=100, null=True)),
                ('client_secret', models.CharField(blank=True, max_length=200, null=True)),
                ('client_id', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Userdata',
            fields=[
                ('userID', models.AutoField(primary_key=True, serialize=False)),
                ('personal_email', models.EmailField(blank=True, max_length=70, null=True, unique=True)),
                ('Username', models.CharField(max_length=120)),
            ],
        ),
        migrations.AddField(
            model_name='availabledata',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capi.Userdata'),
        ),
        migrations.AddField(
            model_name='assignementdata',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='capi.Userdata'),
        ),
    ]
