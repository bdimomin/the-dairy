# Generated by Django 4.2.3 on 2023-10-14 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_renewal_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='renewal_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
