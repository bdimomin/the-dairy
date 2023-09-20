# Generated by Django 4.2.3 on 2023-09-19 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_renewal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.CharField(choices=[('domain registration', 'Domain Registration'), ('domain renewal', 'Domain Renewal'), ('hosting registration', 'Hosting Registration'), ('hosting renewal', 'Hosting Renewal')], max_length=50)),
                ('amount', models.FloatField()),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
    ]