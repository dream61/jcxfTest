from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    name = forms.CharField(label="项目名称")
    desc = forms.CharField(label="项目描述")
    proj_owner = forms.CharField(label="项目负责人")
    test_owner = forms.CharField(label="测试负责人")
    dev_owner = forms.CharField(label="开发负责人")
    class Meta:
        model = Project
        fields = ['name', 'desc','proj_owner','test_owner','dev_owner']
