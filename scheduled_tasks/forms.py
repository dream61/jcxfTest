from django import forms
from .models import ScheduledTask,TestScenario,Users
from django.utils.timezone import now


class ScheduledTaskForm(forms.ModelForm):
    class Meta:
        model = ScheduledTask
        fields = ['name', 'testscenario', 'cron_expression','email']
    
    widgets = {
            'cron_expression': forms.TextInput(attrs={
                'placeholder': '请输入CRON表达式 (例如: * * * * *)',
                'class': 'form-control'
            })
        }

    name = forms.CharField(
        label='任务名称',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    testscenario = forms.ModelChoiceField(
        label='测试场景',
        queryset=TestScenario.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )




    def clean_task_time(self):
        task_time = self.cleaned_data.get('task_time')
        if task_time < now():
            raise forms.ValidationError("执行时间不能早于当前时间")
        return task_time
