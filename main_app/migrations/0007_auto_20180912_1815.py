# Generated by Django 2.0.3 on 2018-09-12 12:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20180912_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 12, 12, 45, 0, 431086, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 12, 12, 45, 0, 430059, tzinfo=utc)),
        ),
    ]
