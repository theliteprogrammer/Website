# Generated by Django 4.2.4 on 2023-08-23 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_wasteitem_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteitem',
            name='disposal_instructions',
            field=models.TextField(blank=True, null=True),
        ),
    ]
