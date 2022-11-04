from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse
import re


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当用户请求进入时触发执行
        :param request:
        :return:
        """

        # 获取当前用户请求的url
        current_url = request.path_info

        # 判断用户访问的url是否在白名单中，如果是直接继续，无需验证
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                return None

        # 获取当前用户在session中保存的权限列表
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return HttpResponse("未获取到用户权限信息，请登录！！！")

        url_record = [
            {'title': '首页', 'url': '#'}
        ]

        # 此处代码进行判断
        for url in settings.NO_PERMISSION_LIST:
            if re.match(url, request.path_info):
                # 需要登录，但无需权限校验
                request.current_selected_permission = 0
                request.breadcrumb = url_record

                return None



        # 权限信息的匹配
        flag = False

        for item in permission_dict.values():
            reg = "^%s$" % item['url']
            if re.match(reg, current_url):
                flag = True
                request.current_selected_permission = item['pid'] or item['id']

                if not item['pid']:
                    url_record.extend([
                        {'title': item['title'], 'url': item['url'], 'class': 'active'}
                    ])
                else:
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'}
                    ])
                request.breadcrumb = url_record
                break
        if not flag:
            return HttpResponse("无权访问")
