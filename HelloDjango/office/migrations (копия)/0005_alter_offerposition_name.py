# Generated by Django 4.0.1 on 2022-01-24 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0004_offerposition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerposition',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название оффера'),
        ),
    ]
