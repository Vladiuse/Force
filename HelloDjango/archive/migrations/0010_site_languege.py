# Generated by Django 4.0.1 on 2022-05-11 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0009_remove_site_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='languege',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive.languege', verbose_name='Язык сайта'),
        ),
    ]
