# Generated by Django 5.0.7 on 2024-07-28 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Youme', '0032_alter_utilisateur_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2024, 7, 28, 17, 14, 11, 538587)),
        ),
    ]
