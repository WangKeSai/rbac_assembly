from django.conf import settings
from django.db import IntegrityError
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from collections import OrderedDict

from django.utils.module_loading import import_string

from rbac import models
from rbac.form.menu import MenuModelForm, SencondMenuModelForm, PermissionModelForm, MutliAddPermissionForm, MutliEditPermissionForm
from rbac.service.make_urls import make_urls
from rbac.service.routes import get_all_url_dict


def menu_list(request):
    """
    一级菜单列表
    :param request:
    :return:
    """
    menu_queryset = models.Menu.objects.all()
    menu_id = request.GET.get("mid")
    second_menu_id = request.GET.get("sid")
    menu_obj = models.Menu.objects.filter(id=menu_id)
    permission_obj = models.Permission.objects.filter(pid=second_menu_id)
    if not permission_obj:
        second_menu_id = None
    if not menu_obj:
        menu_id = None
    if menu_id:
        second_menu = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menu = []
    if second_menu_id:
        permission = models.Permission.objects.filter(pid=second_menu_id)
    else:
        permission = []
    return render(request, 'rbac/menu_list.html', {'menu_list': menu_queryset, "menu_id": menu_id, 'second_menu': second_menu, 'second_menu_id': second_menu_id, 'permission':permission})


def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """

    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        url = make_urls(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, rid):
    """
    编辑一级菜单
    :param request:
    :param rid:
    :return:
    """
    obj = models.Menu.objects.get(id=rid)
    if not obj:
        return HttpResponse("用户不存在！")
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        url = make_urls(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def menu_del(request, rid):
    """
    删除一级菜单
    :param request:
    :param rid:
    :return:
    """

    url = make_urls(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Menu.objects.filter(id=rid).delete()
    return redirect(url)


def second_menu_add(request, menu_id):
    """
    添加二级菜单
    :param request:
    :param menu_id:
    :return:
    """
    menu = models.Menu.objects.filter(id=menu_id).first()
    if request.method == 'GET':
        form = SencondMenuModelForm(initial={"menu":menu})
        return render(request, 'rbac/change.html', {'form': form})
    form = SencondMenuModelForm(data=request.POST, initial={"menu_id":menu})
    if form.is_valid():
        form.save()
        url = make_urls(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, rid):
    """
    编辑二级菜单
    :param request:
    :param menu_id:
    :return:
    """
    permission = models.Permission.objects.filter(id=rid).first()
    if request.method == 'GET':
        form = SencondMenuModelForm(instance=permission)
        return render(request, 'rbac/change.html', {'form': form})
    form = SencondMenuModelForm(data=request.POST, instance=permission)
    if form.is_valid():
        form.save()
        url = make_urls(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_del(request, rid):
    """
    删除二级菜单
    :param request:
    :param rid:
    :return:
    """

    url = make_urls(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(id=rid).delete()
    return redirect(url)


def permission_add(request, second_menu_id):
    """
    增加权限
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        second_menu = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu:
            return HttpResponse("二级菜单不存在，请重新选择！")
        form.instance.pid = second_menu
        form.save()
        url = make_urls(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})



def permission_edit(request, rid):
    """
    编辑权限
    :param request:
    :param second_menu_id:
    :return:
    """
    permission = models.Permission.objects.filter(id=rid).first()
    if request.method == 'GET':
        form = PermissionModelForm(instance=permission)
        return render(request, 'rbac/change.html', {'form': form})
    form = PermissionModelForm(data=request.POST, instance=permission)
    if form.is_valid():
        form.save()
        url = make_urls(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def permission_del(request, rid):
    """
    删除权限
    :param request:
    :param second_menu_id:
    :return:
    """
    url = make_urls(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(id=rid).delete()
    return redirect(url)


def multi_permission(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    generate_formset_class = formset_factory(MutliAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MutliEditPermissionForm, extra=0)
    generate_formset = None
    update_formset = None

    post_type = request.GET.get("type")

    if request.method == 'POST' and post_type == 'generate':
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            name_list = []
            post_row_list = formset.cleaned_data
            has_erroe = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]

                if row_dict['name'] in name_list:
                    formset.errors[i].update({"name": ["输入了相同的别名"]})
                    generate_formset = formset
                    has_erroe = True
                    break
                name_list.append(row_dict['name'])
                try:
                    new_object = models.Permission(**row_dict)
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    has_erroe = True
                    formset.errors[i].update(e)
                    generate_formset = formset
            if not has_erroe:
                pass
                models.Permission.objects.bulk_create(object_list, batch_size=100)

        else:

            generate_formset = formset


    if request.method == 'POST' and post_type == 'update':
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    row_object = models.Permission.objects.filter(id=permission_id).first()
                    for k,v in row_dict.items():
                        setattr(row_object, k, v)
                    row_object.validate_unique()
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
                    print(formset.errors)
        else:
            update_formset = formset



    all_url_dict = get_all_url_dict()
    router_name_set = set(all_url_dict.keys())
    permissions = models.Permission.objects.all().values('id','title','name','url','menu_id', 'pid_id')
    permission_dict = OrderedDict()
    permission_name_set = set()
    for row in permissions:
        permission_dict[row['name']] = row
        permission_name_set.add(row['name'])
    for name,value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = "路由和数据库中不一致"
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set

        generate_formset = generate_formset_class(initial=[row_dict for name,row_dict in all_url_dict.items() if name in generate_name_list])

    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]
    if not update_formset:
        update_name_list = permission_name_set & router_name_set

        update_formset = update_formset_class(initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list])
    return render(request, 'rbac/multi_permission.html',
                  {"generate_formset": generate_formset,
                   "delete_row_list": delete_row_list,
                   "update_formset": update_formset})


def multi_permission_del(request,rid):
    url = make_urls(request, 'rbac:multi_permission')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(id=rid).delete()
    return redirect(url)


def distribute_permission(request):
    """
    权限分配
    :param request:
    :return:
    """

    user_id = request.GET.get('uid')

    user_object = models.UserInfo.objects.filter(id=user_id).first()
    if not user_object:
        user_id = None

    role_id = request.GET.get('rid')
    role_object = models.Role.objects.filter(id=role_id).first()
    if not role_object:
        role_id = None

    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        # 用户和角色关系添加到第三张表（关系表）
        if not user_object:
            return HttpResponse('请选择用户，然后再分配角色！')
        user_object.roles.set(role_id_list)

    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('请选择角色，然后再分配权限！')
        role_object.permissions.set(permission_id_list)

    # 获取当前用户拥有的所有角色
    if user_id:
        user_has_roles = user_object.roles.all()
    else:
        user_has_roles = []

    user_has_roles_dict = {item.id: None for item in user_has_roles}

    # 获取当前用户用户用户的所有权限

    # 如果选中的角色，优先显示选中角色所拥有的权限
    # 如果没有选择角色，才显示用户所拥有的权限
    if role_object:  # 选择了角色
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}

    elif user_object:  # 未选择角色，但选择了用户
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id',
                                                                                              'permissions').distinct()
        user_has_permissions_dict = {item['permissions']: None for item in user_has_permissions}
    else:
        user_has_permissions_dict = {}

    all_user_list = models.UserInfo.objects.all()

    all_role_list = models.Role.objects.all()

    menu_permission_list = []

    # 所有的菜单（一级菜单）
    all_menu_list = models.Menu.objects.values('id', 'title')
    """
    [
        {id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,'children':[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1 },]},
        {id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2 },{id:5,title:x1, menu_id:2 },]},
        {id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3 },]},
    ]
    """
    all_menu_dict = {}
    """
       {
           1:{id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1,children:[] },]},
           2:{id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2,children:[] },{id:5,title:x1, menu_id:2,children:[] },]},
           3:{id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3,children:[] },]},
       }
       """
    for item in all_menu_list:
        item['children'] = []
        all_menu_dict[item['id']] = item

    # 所有二级菜单
    all_second_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')

    """
    [
        {id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
        {id:2,title:x1, menu_id:1,children:[] },
        {id:3,title:x1, menu_id:2,children:[] },
        {id:4,title:x1, menu_id:3,children:[] },
        {id:5,title:x1, menu_id:2,children:[] },
    ]
    """
    all_second_menu_dict = {}
    """
        {
            1:{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
            2:{id:2,title:x1, menu_id:1,children:[] },
            3:{id:3,title:x1, menu_id:2,children:[] },
            4:{id:4,title:x1, menu_id:3,children:[] },
            5:{id:5,title:x1, menu_id:2,children:[] },
        }
        """
    for row in all_second_menu_list:
        row['children'] = []
        all_second_menu_dict[row['id']] = row

        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)

    # 所有三级菜单（不能做菜单的权限）
    all_permission_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')
    """
    [
        {id:11,title:x2,pid:1},
        {id:12,title:x2,pid:1},
        {id:13,title:x2,pid:2},
        {id:14,title:x2,pid:3},
        {id:15,title:x2,pid:4},
        {id:16,title:x2,pid:5},
    ]
    """
    for row in all_permission_list:
        pid = row['pid_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(row)

    """
    [
        {
            id:1,
            title:'业务管理'
            children:[
                {
                    'id':11, 
                    title:'账单列表',
                    children:[
                        {'id':12,title:'添加账单'}
                    ]
                },
                {'id':11, title:'客户列表'},
            ]
        },

    ]
    """

    return render(
        request,
        'rbac/distribute_permission.html',
        {
            'user_list': all_user_list,
            'role_list': all_role_list,
            'all_menu_list': all_menu_list,
            'user_id': user_id,
            'role_id': role_id,
            'user_has_roles_dict': user_has_roles_dict,
            'user_has_permissions_dict': user_has_permissions_dict,
        }
    )
