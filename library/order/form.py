from datetime import datetime

from django.forms import ModelForm

from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'plated_end_at']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # self.fields['end_at'].required = False
        self.fields['plated_end_at'].initial = datetime.now()


class OrderEndAtForm(ModelForm):
    class Meta:
        model = Order
        fields = ['end_at']

    def __init__(self, *args, **kwargs):
        super(OrderEndAtForm, self).__init__(*args, **kwargs)
        self.fields['end_at'].required = True
