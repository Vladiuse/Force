# Generated by Django 4.0.1 on 2022-01-26 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0007_remove_copypaste_data_copypastedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='copypaste',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название копипасты'),
        ),
    ]
