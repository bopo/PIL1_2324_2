# Generated by Django 4.2.13 on 2024-06-19 16:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Youme', '0028_alter_utilisateur_last_login_privateroom_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('discussion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Youme.discussion')),
            ],
        ),
        migrations.RemoveField(
            model_name='privateroom',
            name='participants',
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name=datetime.datetime(2024, 6, 19, 17, 21, 19, 501327)),
        ),
        migrations.DeleteModel(
            name='PrivateMessage',
        ),
        migrations.DeleteModel(
            name='PrivateRoom',
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='discussion',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discussion_user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='discussion',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discussion_user2', to=settings.AUTH_USER_MODEL),
        ),
    ]
