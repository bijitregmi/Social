# Generated by Django 4.1.7 on 2024-01-24 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='followed_by', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
