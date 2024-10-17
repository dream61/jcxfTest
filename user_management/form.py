# forms.py
from django import forms
from .models import Users

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="确认密码")
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'confirm_password','status', 'project', 'module', 'is_staff', 'is_superuser']
        widgets = {
            'password': forms.PasswordInput(),  # 密码字段以密码形式输入
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "密码和确认密码不一致，请重新输入。")
            #raise forms.ValidationError("密码和确认密码不一致，请重新输入。")
        

