# Generated by Django 3.0.3 on 2020-03-17 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tahunmasuk',
            field=models.CharField(default='-', max_length=50, verbose_name='Tahun Masuk'),
        ),
    ]