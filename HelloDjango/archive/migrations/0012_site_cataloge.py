# Generated by Django 4.0.1 on 2022-05-11 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0011_alter_site_category_cataloge'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='cataloge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive.cataloge'),
        ),
    ]
