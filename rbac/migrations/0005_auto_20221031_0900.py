# Generated by Django 3.2 on 2022-10-31 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_permission_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='一级菜单名称')),
                ('icon', models.CharField(blank=True, max_length=32, null=True, verbose_name='图标')),
            ],
        ),
        migrations.RemoveField(
            model_name='permission',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='permission',
            name='is_menu',
        ),
        migrations.AddField(
            model_name='permission',
            name='menu',
            field=models.ForeignKey(blank=True, help_text='null表示不是菜单，非null表示是二级菜单', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rbac.menu', verbose_name='所属菜单'),
        ),
    ]