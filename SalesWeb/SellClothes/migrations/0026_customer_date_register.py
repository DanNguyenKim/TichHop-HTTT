# Generated by Django 4.1.2 on 2022-12-06 10:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SellClothes', '0025_product_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='date_register',
            field=models.DateField(default=datetime.datetime.today, verbose_name='Ngày đăng ký'),
        ),
    ]