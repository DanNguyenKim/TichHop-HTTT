# Generated by Django 4.1.2 on 2022-12-13 10:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SellClothes', '0035_alter_comment_time_cmt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_cmt',
            field=models.DateField(default=datetime.datetime.today, verbose_name='Ngày phản hồi'),
        ),
    ]