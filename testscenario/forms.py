from django import forms
from .models import TestScenario

class TestSceniorForm(forms.ModelForm):
    class Meta:
        model = TestScenario
        fields = ['name', 'description', 'test_cases']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '场景名称'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '描述'}),
            'test_cases': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': '场景名称',
            'description': '描述',
            'test_cases': '选择测试用例',
        }

    
