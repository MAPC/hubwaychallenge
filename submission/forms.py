from django import forms
from django.core.exceptions import ValidationError

from simplemathcaptcha.fields import MathCaptchaField

from models import Entry
    
class EntryForm(forms.ModelForm):

    rules = forms.BooleanField(
        error_messages={'required': 'You must agree to the Rules to submit.'}
    )
    captcha = MathCaptchaField(required=True)

    # custom validatons
    def clean_screenshot(self):
         screenshot = self.cleaned_data.get('screenshot',False)
         if screenshot:
             if screenshot._size > 20*1024*1024:
                   raise ValidationError("Image file is too large, max. 20MB allowed.")
             return screenshot
    def clean_file(self):
         file = self.cleaned_data.get('file',False)
         if file:
             if file._size > 20*1024*1024:
                   raise ValidationError("File is too large, max. 20MB allowed.")
             return file

    class Meta:
        model = Entry
        fields = ('name', 'email', 'description', 'screenshot', 'file', 'url', 'rules')
