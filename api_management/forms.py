from django import forms
from .models import ApiInterface

class ApiForm(forms.ModelForm):
    class Meta:
        model = ApiInterface
        fields = ["name","project", "module", "url","headers","request_method","status","request_params","response_params","desc"]
