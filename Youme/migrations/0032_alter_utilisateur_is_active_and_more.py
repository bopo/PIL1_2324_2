# Generated by Django 4.2.13 on 2024-06-20 06:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Youme', '0031_alter_utilisateur_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2024, 6, 20, 7, 35, 27, 973889)),
        ),
    ]
