# Generated by Django 2.1.2 on 2018-11-25 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_auto_20181119_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='restrictions',
            field=models.ManyToManyField(blank=True, to='map.Limitation'),
        ),
    ]
