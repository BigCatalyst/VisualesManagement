# Generated by Django 3.1.12 on 2021-07-14 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genderdocumental',
            name='type',
            field=models.TextField(blank=True, db_column='TipoDocumental', null=True),
        ),
    ]