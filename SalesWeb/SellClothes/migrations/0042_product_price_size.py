# Generated by Django 4.1.2 on 2023-01-14 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SellClothes', '0041_pricesize'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='SellClothes.pricesize', verbose_name='Khoảng giá'),
        ),
    ]
