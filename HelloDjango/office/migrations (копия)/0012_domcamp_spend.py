# Generated by Django 4.0.1 on 2022-02-26 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0011_alter_country_phone_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomCamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=50, verbose_name='Домен')),
            ],
        ),
        migrations.CreateModel(
            name='Spend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('spend', models.FloatField()),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='office.domcamp')),
            ],
        ),
    ]
