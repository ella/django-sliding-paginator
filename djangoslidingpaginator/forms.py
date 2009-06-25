from django import forms

class PaginationForm(forms.Form):
    on_page = forms.IntegerField(widget=forms.TextInput(attrs={'size':'3'}))
