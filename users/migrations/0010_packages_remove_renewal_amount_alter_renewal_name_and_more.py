# Generated by Django 4.2.3 on 2023-09-28 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_status_alter_expenses_purpose'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('duratioin', models.IntegerField()),
                ('price', models.FloatField()),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='renewal',
            name='amount',
        ),
        migrations.AlterField(
            model_name='renewal',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Trash', 'Trash'), ('Terminate', 'Terminate')], default='Active', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='renewal',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.packages'),
        ),
    ]
