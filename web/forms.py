from django import forms


class SearchForm(forms.Form):
    destination = forms.CharField()
    location = forms.CharField()
