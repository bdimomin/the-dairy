# Generated by Django 4.2.3 on 2023-10-07 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_rename_start_date_renewal_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renewal',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
