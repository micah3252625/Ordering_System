from django import forms

TRANSACTION_CHOICES = (
    ('Delivery', 'Delivery'),
    ('Pick up', 'Pick up'),
)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'firstName',
    }))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'lastName',
    }))
    contact = forms.CharField(max_length=11, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'contact',
        'placeholder': '09958200176',
    }))
    street = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'street',
        'placeholder': '1234 Main St',
    }))
    barangay = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'barangay',
        'placeholder': 'Yakan Village / Upper Calarian',
    }))
    text = forms.CharField(max_length=250, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'id': 'text',
        'rows': 4,
    }))

    money = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Change for e.g 1000',
        }))
