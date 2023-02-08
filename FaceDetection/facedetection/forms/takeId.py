from django import forms

class takeId(forms.Form):
    id = forms.IntegerField()
    name = forms.CharField()