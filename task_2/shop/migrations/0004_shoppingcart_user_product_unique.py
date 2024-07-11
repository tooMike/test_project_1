# Generated by Django 3.2.16 on 2024-07-10 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_shoppingcart'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='user_product_unique'),
        ),
    ]
