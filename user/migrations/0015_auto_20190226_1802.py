# Generated by Django 2.1.7 on 2019-02-26 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20190224_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]