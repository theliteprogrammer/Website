from django import forms
from core.models import WasteItem


class WasteItemForm(forms.ModelForm):

    class Meta:
        model = WasteItem
        fields = ['name', 'category', 'disposal_instructions', 'hazardous', 'recyclable']
