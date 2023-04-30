from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(required=False, initial=1, widget=forms.NumberInput(attrs={
        'min': '1',
        'class': 'form-control',
    }))
