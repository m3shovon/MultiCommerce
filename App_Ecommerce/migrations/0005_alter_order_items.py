# Generated by Django 5.1.3 on 2024-12-09 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_Ecommerce', '0004_remove_order_address_remove_order_customer_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orders', to='App_Ecommerce.cartitem'),
        ),
    ]
