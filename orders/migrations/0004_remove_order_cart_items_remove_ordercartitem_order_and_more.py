# Generated by Django 5.1.6 on 2025-02-15 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_products_ordercartitem_order_cart_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart_items',
        ),
        migrations.RemoveField(
            model_name='ordercartitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='ordercartitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='ordercartitem',
            name='quantity',
        ),
    ]
