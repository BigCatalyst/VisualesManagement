# Generated by Django 3.2.9 on 2021-11-05 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0003_auto_20211104_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='photo',
            field=models.ImageField(blank=True, db_column='Foto', max_length=2500, null=True, upload_to='ofertas/', verbose_name='Foto'),
        ),
    ]