# Generated by Django 4.2.6 on 2023-10-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('manufacturer', models.CharField(max_length=100)),
                ('style', models.CharField(max_length=50)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('qty_on_hand', models.PositiveIntegerField()),
                ('commission_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
