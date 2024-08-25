# Generated by Django 5.0.7 on 2024-08-25 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_gmeetclass_created_by_gmeetclass_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='classnote',
            name='for_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='main.schoolclass'),
            preserve_default=False,
        ),
    ]
