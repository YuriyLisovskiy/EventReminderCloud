# Generated by Django 2.1.5 on 2019-02-28 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20190226_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='lang',
            field=models.CharField(default='en_US', max_length=5),
        ),
    ]
