from django import forms


class UrlForm(forms.Form):
    url = forms.URLField(required=True)
    hashed_url = forms.CharField(required=False, max_length=10)
