# Generated by Django 2.2.3 on 2019-07-29 15:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0008_auto_20190729_1832'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Replies',
            new_name='Reply',
        ),
    ]
