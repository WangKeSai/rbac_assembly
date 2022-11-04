from django.http import QueryDict
from django.urls import reverse


def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的url
    :param request:
    :return:
    """

    basic_url = reverse(name, args=args, kwargs=kwargs)
    if not request.GET:
        return basic_url
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()
    return "%s?%s" % (basic_url, query_dict.urlencode())


def make_urls(request, name, *args, **kwargs):
    """
    反向生成带有参数的url
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    """
    url = reverse(name, args=args, kwargs=kwargs)
    origin_url = request.GET.get("_filter")
    if origin_url:
        url = "%s?%s" % (url, origin_url)
    return url