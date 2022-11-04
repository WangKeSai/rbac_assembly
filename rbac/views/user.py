from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from rbac import models
from django import forms

from rbac.form.user import UserModelForm, EditUserModelForm, ResetUserModelForm


def user_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_queryset = models.UserInfo.objects.all()
    return render(request, 'rbac/user_list.html', {'users': role_queryset})


def user_add(request):
    """
    添加角色
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, rid):
    """
    编辑角色
    :param request:
    :return:
    """

    obj = models.UserInfo.objects.get(id=rid)
    if not obj:
        return HttpResponse("用户不存在！")
    if request.method == 'GET':
        form = EditUserModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = EditUserModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_reset_password(request, rid):
    """
    重置密码
    :param request:
    :return:
    """
    obj = models.UserInfo.objects.filter(id=rid).first()
    if not obj:
        return HttpResponse("用户不存在！")
    if request.method == 'GET':
        form = ResetUserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = ResetUserModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_del(request, rid):
    """
    删除角色
    :param request:
    :return:
    """
    origin_url = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    models.UserInfo.objects.filter(id=rid).delete()
    return redirect(origin_url)
