# Generated by Django 3.2.9 on 2021-12-24 06:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_images_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500, verbose_name='Dirección')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phones', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=15), size=2)),
            ],
        ),
    ]