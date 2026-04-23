from django import forms
from .models import HostList

class AccessForm(forms.Form):
    host = forms.ModelChoiceField(
        queryset=HostList.objects.all(),
        required=True,
        label="Select Host"
    )
    # Removed 'purpose' because we’ll get it from the session.
