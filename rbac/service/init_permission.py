from django.conf import settings

def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user:  当前用户对象
    :param request:  请求相关所有数据
    :return: 
    """

    # 根据当前用户信息获取到该用户所拥有的所有权限，并放入session

    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__title",
                                                                                      "permissions__name",
                                                                                      "permissions__pid",
                                                                                      "permissions__title",
                                                                                      "permissions__pid__title",
                                                                                      "permissions__pid__url",
                                                                                      "permissions__url",
                                                                                      "permissions__menu_id",
                                                                                      "permissions__menu__title",
                                                                                      "permissions__menu__icon").distinct()
    # 菜单列表
    menu_dict = {}
    # 权限列表
    permission_list = {}
    for item in permission_queryset:

        permission_list[item['permissions__name']] = {'id': item['permissions__id'],
                                'title': item['permissions__title'],
                                'url':item['permissions__url'],
                                'pid':item['permissions__pid'],
                                'p_title':item['permissions__pid__title'],
                                'p_url':item['permissions__pid__url']}

        menu_id = item['permissions__menu_id']
        if not menu_id:
            continue
        node = {'id': item['permissions__id'], 'title': item['permissions__title'], 'url': item['permissions__url']}
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [node, ]
            }

    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict