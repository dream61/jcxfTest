from django import forms
from .models import TestCase

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ["relate_api","name", "host_url","request_method", "url", "headers", "request_data", "body", "expected_response", "extract_var", "description"]

    
