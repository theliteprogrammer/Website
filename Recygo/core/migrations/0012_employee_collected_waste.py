# Generated by Django 4.2.4 on 2023-08-25 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_employee_alter_wasteorder_collector'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='collected_waste',
            field=models.ManyToManyField(to='core.wasteorder'),
        ),
    ]
