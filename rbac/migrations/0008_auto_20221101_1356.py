# Generated by Django 3.2 on 2022-11-01 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0007_permission_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(default='1', max_length=32, verbose_name='图标'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(default=1, max_length=32, unique=True, verbose_name='URL别名'),
            preserve_default=False,
        ),
    ]
