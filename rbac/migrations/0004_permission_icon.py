# Generated by Django 3.2 on 2022-10-30 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0003_permission_is_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='icon',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='图标'),
        ),
    ]
