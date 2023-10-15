# Generated by Django 4.2.3 on 2023-10-15 07:36

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_aboutpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pricingpage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('content', tinymce.models.HTMLField()),
            ],
        ),
    ]
