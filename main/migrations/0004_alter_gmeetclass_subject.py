# Generated by Django 5.0.7 on 2024-09-04 03:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_schoolclass_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmeetclass',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gmeet_classes', to='main.subject'),
        ),
    ]
