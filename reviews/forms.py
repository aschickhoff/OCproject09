from django import forms
from .models import Ticket, Review


class CreateTicket(forms.ModelForm):
    title = forms.CharField(max_length=128, widget=forms.TextInput)
    description = forms.CharField(max_length=2048, widget=forms.Textarea(), required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class CreateReview(forms.ModelForm):
    headline = forms.CharField(max_length=128, widget=forms.TextInput())
    rating = forms.ChoiceField(initial=1, widget=forms.RadioSelect(), choices=((1, "★"), (2, "★★"), (3, "★★★"), (4, "★★★★"), (5, "★★★★★")))
    body = forms.CharField(max_length=8192, widget=forms.Textarea(), required=False)

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
