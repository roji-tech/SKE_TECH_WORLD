# Generated by Django 5.0.7 on 2024-09-15 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_gmeetclass_end_time_gmeetclass_duration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='academic_year',
            new_name='session_admitted',
        ),
        migrations.RemoveField(
            model_name='student',
            name='admission_date',
        ),
    ]