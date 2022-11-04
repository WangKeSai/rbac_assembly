from django.db import models


# Create your models here.
class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(max_length=32, verbose_name='一级菜单名称')
    icon = models.CharField(max_length=32, verbose_name='图标')

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')
    email = models.CharField(max_length=32, verbose_name='邮箱')
    roles = models.ManyToManyField(to='Role', blank=True, verbose_name='拥有的所有角色')

    def __str__(self):
        return self.name


class Role(models.Model):
    title = models.CharField(max_length=20, verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission', blank=True, verbose_name='拥有的所有权限')

    def __str__(self):
        return self.title


class Permission(models.Model):
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(max_length=128, verbose_name='包含正则的URL')
    name = models.CharField(verbose_name='URL别名', max_length=32, unique=True)
    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', null=True, blank=True, help_text='null表示不是菜单，非null表示是二级菜单', on_delete=models.DO_NOTHING)
    pid = models.ForeignKey(verbose_name='关联的权限', to='Permission', help_text='对于非菜单权限需要选择一个可以成为菜单的权限', null=True, blank=True, related_name='parents', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
