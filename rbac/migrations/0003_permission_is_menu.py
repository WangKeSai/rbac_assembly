# Generated by Django 3.2 on 2022-10-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_delete_usersrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='is_menu',
            field=models.BooleanField(default=False, verbose_name='是否可做菜单'),
        ),
    ]
