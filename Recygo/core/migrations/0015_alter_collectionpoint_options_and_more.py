# Generated by Django 4.2.4 on 2023-08-27 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_wasteplan_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collectionpoint',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='wasteitem',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='wasteorder',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='wasteplan',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('Driver', 'Driver'), ('Collector', 'Collector'), ('Sorter', 'Sorter'), ('Recycling Specialist', 'Recycling Specialist'), ('Route Planner', 'Route Planner'), ('Dispatcher', 'Dispatcher'), ('Supervisor', 'Supervisor'), ('Maintenance Technician', 'Maintenance Technician')], default='Collector', max_length=200),
        ),
    ]
