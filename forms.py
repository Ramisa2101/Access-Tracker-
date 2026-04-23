from django import forms
from .models import UserDetails

class VisitorLookupForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    contact_no = forms.CharField(max_length=20, required=True)
    
class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = [
            'name',
            'contact_no',
            'designation',
            'company_name',
            'company_no',
            'address',
            'company_address',
            'date_of_birth',
            'nid_passport',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
# In your forms.py — same styling as before
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
        if isinstance(field.widget, forms.Textarea):
            field.widget.attrs.update({
                'class': 'w-full px-5 py-4 border border-gray-300 rounded-xl focus:ring-4 focus:ring-amber-200 focus:border-amber-500 outline-none transition resize-none',
                'rows': 2,
            })
        else:
            field.widget.attrs.update({
                'class': 'w-full px-5 py-4 border border-gray-300 rounded-xl focus:ring-4 focus:ring-amber-200 focus:border-amber-500 outline-none transition text-lg',
            })