# Generated by Django 5.0.7 on 2024-08-01 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0004_researchpaper_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchpaper',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
