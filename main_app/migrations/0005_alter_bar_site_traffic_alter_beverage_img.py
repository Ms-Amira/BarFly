# Generated by Django 4.2 on 2023-04-20 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_remove_photo_beverages_beverage_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bar',
            name='site_traffic',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='beverage',
            name='img',
            field=models.URLField(default='', max_length=500),
        ),
    ]