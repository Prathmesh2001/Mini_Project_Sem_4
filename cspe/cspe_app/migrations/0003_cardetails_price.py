# Generated by Django 3.1.3 on 2021-04-14 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cspe_app', '0002_auto_20210411_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardetails',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
