# Generated by Django 4.2.4 on 2023-08-27 16:45

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='did',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvxyz', blank=True, length=15, max_length=20, null=True, prefix=''),
        ),
    ]
