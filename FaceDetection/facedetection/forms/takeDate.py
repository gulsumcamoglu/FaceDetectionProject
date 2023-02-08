from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class LastActiveForm(forms.Form):
    """
    Last Active Date Form
    """
    choose_day = forms.DateField(widget=DateInput)
    