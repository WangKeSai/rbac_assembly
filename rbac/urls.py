from django.conf.urls import url,include
from django.contrib import admin
from rbac.views import role, user, menu


urlpatterns = [
    url(r'^role/list/$', role.role_list, name='role_list'),
    url(r'^role/add/$', role.role_add, name='role_add'),
    url(r'^role/edit/(?P<rid>\d+)/$', role.role_edit, name='role_edit'),
    url(r'^role/del/(?P<rid>\d+)/$', role.role_del, name='role_del'),

    url(r'^user/list/$', user.user_list, name='user_list'),
    url(r'^user/add/$', user.user_add, name='user_add'),
    url(r'^user/edit/(?P<rid>\d+)/$', user.user_edit, name='user_edit'),
    url(r'^user/del/(?P<rid>\d+)/$', user.user_del, name='user_del'),
    url(r'^user/reset/password/(?P<rid>\d+)/$', user.user_reset_password, name='user_reset_password'),

    url(r'^menu/list/$', menu.menu_list, name='menu_list'),
    url(r'^menu/menu/add/$', menu.menu_add, name='menu_add'),
    url(r'^menu/edit/(?P<rid>\d+)/$', menu.menu_edit, name='menu_edit'),
    url(r'^menu/del/(?P<rid>\d+)/$', menu.menu_del, name='menu_del'),

    url(r'^second/menu/add/(?P<menu_id>\d+)/$', menu.second_menu_add, name='second_menu_add'),
    url(r'^second/menu/edit/(?P<rid>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),
    url(r'^second/menu/del/(?P<rid>\d+)/$', menu.second_menu_del, name='second_menu_del'),

    url(r'^permission/add/(?P<second_menu_id>\d+)/$', menu.permission_add, name='permission_add'),
    url(r'^permission/edit/(?P<rid>\d+)/$', menu.permission_edit, name='permission_edit'),
    url(r'^permission/del/(?P<rid>\d+)/$', menu.permission_del, name='permission_del'),

    url(r'^multi/permission/$', menu.multi_permission, name='multi_permission'),
    url(r'^multi/permission/del/(?P<rid>\d+)/$', menu.multi_permission_del, name='multi_permission_del'),

    url(r'^distribute/permission/$', menu.distribute_permission, name='distribute_permission'),
]