# Generated by Django 3.2.9 on 2021-11-05 02:51

from django.db import migrations
import pgcrypto.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_alter_license_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='expired',
            field=pgcrypto.fields.EncryptedDateTimeField(blank=True, charset='utf-8', check_armor=True, cipher='aes', null=True, versioned=False),
        ),
    ]