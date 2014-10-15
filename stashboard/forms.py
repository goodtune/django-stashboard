from django import forms

from .models import Service


class RSSQueryForm(forms.Form):
    "Filter query string for RSS feed."
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(), required=False)
