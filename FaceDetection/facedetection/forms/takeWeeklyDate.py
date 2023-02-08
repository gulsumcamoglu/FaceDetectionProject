from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class LastActiveFormWeekly(forms.Form):
    """
    Last Active Date Form
    """
    first_date = forms.DateField(widget=DateInput)
    last_date  = forms.DateField(widget=DateInput)
    