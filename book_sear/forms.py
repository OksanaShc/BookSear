from django import forms


class SearchForm(forms.Form):
    target_text = forms.CharField(label='What we will search  in books?', max_length=100, required=True, min_length=1)
    e_mail = forms.EmailField()
