# Generated by Django 3.2.9 on 2021-11-24 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_shopcart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcart',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
