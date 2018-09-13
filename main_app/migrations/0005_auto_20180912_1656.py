# Generated by Django 2.0.3 on 2018-09-12 11:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20180912_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='answer',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 12, 11, 26, 8, 103716, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 12, 11, 26, 8, 102713, tzinfo=utc)),
        ),
    ]
