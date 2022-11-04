from django import forms
from django.utils.safestring import mark_safe

from rbac import models


class MenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = ['title', 'icon']
        widgets = {'title': forms.TextInput(attrs={"class": "form-control"}),
                   "icon": forms.RadioSelect(
                       choices=[
                           ['fa-calendar', mark_safe('<i class="fa fa-calendar" aria-hidden="true"></i>')],
                           ['fa-calendar-times-o',
                            mark_safe('<i class="fa fa-calendar-times-o" aria-hidden="true"></i>')],
                           ['fa-book', mark_safe('<i class="fa fa-book" aria-hidden="true"></i>')],
                           ['fa-drivers-license-o',
                            mark_safe('<i class="fa fa-drivers-license-o" aria-hidden="true"></i>')],
                           ['fa fa-folder-open', mark_safe('<i class="fa fa-folder-open" aria-hidden="true"></i>')],
                       ]
                   )}


class SencondMenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        exclude = ['pid']

    def __init__(self, *args, **kwargs):
        super(SencondMenuModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PermissionModelForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        exclude = ['menu', 'pid']

    def __init__(self, *args, **kwargs):
        super(PermissionModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MutliAddPermissionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-------')],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-------')],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list("id", "title")
        self.fields["pid_id"].choices += models.Permission.objects.filter(pid__isnull=True).exclude(menu__isnull=True).values_list("id", "title")


class MutliEditPermissionForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-------')],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-------')],
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list("id", "title")
        self.fields["pid_id"].choices += models.Permission.objects.filter(pid__isnull=True).exclude(menu__isnull=True).values_list("id", "title")












