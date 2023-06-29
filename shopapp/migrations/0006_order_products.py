# Generated by Django 4.1.5 on 2023-01-31 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0005_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='shopapp.product'),
        ),
    ]
