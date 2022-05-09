from django import forms


class FollowerForm(forms.Form):
    followed_user = forms.CharField(label=False, widget=forms.TextInput())
