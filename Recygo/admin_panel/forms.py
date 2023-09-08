from django import forms
from django.forms import ImageField, FileInput, DateTimeInput

from core.models import WasteOrder

class DateTimeInput(forms.DateTimeInput):
    input_type = "date"

class WasteOrderForm(forms.ModelForm):

    class Meta:
        model = WasteOrder
        fields = ['collector', 'collected_status', 'date_to_be_collected', 'message_to_subscriber']
        widgets = {
            'date_to_be_collected': DateTimeInput(attrs={'class': ''}),
        }



class CollectionStatusForm(forms.ModelForm):

    class Meta:
        model = WasteOrder
        fields = ['collected_status']
        