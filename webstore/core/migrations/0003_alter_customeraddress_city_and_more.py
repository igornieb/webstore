# Generated by Django 4.1.7 on 2023-02-28 20:37

import core.utilis
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_customeraddress_firstname_customeraddress_lastname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraddress',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='customer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.customer'),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='firstname',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='house_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='lastname',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='postcode',
            field=models.CharField(max_length=50, null=True, validators=[core.utilis.validate_postcode]),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='street',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
