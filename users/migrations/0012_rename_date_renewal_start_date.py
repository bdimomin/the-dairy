# Generated by Django 4.2.3 on 2023-09-28 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_rename_duratioin_packages_duration_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='renewal',
            old_name='date',
            new_name='start_date',
        ),
    ]