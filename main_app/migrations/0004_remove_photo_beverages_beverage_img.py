# Generated by Django 4.2 on 2023-04-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_bar_has_cover_alter_beverage_bev_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='beverages',
        ),
        migrations.AddField(
            model_name='beverage',
            name='img',
            field=models.URLField(default='Enter URL', max_length=500),
        ),
    ]