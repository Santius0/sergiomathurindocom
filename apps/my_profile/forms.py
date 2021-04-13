from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100, required=True)
    email = forms.EmailField(label='Your Email', required=True)
    comment = forms.CharField(label='Your Comment', max_length=500, required=False)
