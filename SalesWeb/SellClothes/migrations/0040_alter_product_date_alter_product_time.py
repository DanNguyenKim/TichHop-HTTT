# Generated by Django 4.1.2 on 2022-12-27 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SellClothes', '0039_alter_comment_commets_other'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateField(verbose_name='Ngày đặt cuối'),
        ),
        migrations.AlterField(
            model_name='product',
            name='time',
            field=models.TimeField(verbose_name='Thời gian đặt cuối'),
        ),
    ]