# Generated by Django 4.2.3 on 2023-10-15 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_remove_homepage_description_homepage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]