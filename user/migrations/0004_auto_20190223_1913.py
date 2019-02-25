# Generated by Django 2.1.7 on 2019-02-23 19:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190223_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(20)]),
        ),
    ]