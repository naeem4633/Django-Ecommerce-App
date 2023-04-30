# Generated by Django 4.1.7 on 2023-04-06 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0009_cart_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total_price',
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(max_length=100)),
                ('cartItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mystore.cartitem')),
            ],
        ),
    ]
