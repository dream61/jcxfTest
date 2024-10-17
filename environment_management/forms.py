from django import forms
from .models import Environment

class EnvironmentForm(forms.ModelForm):
    environment_name = forms.CharField(label="环境名称")
    description = forms.CharField(label="环境描述")
    environment_value = forms.CharField(label="项目负责人")

    class Meta:
        model = Environment
        fields = ['environment_name' , 'environment_value', 'description']
