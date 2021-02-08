from django import forms
import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy

from catalog.models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='yyyy-mm-dd (default : 3weeks later)')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(ugettext_lazy('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(ugettext_lazy('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

class RenewBookModelForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back'] # fields = '__all__' or  exclude = '' // but not recommended
        lables = {'due_back':ugettext_lazy('New renewal date')}
        help_text = {'due_back':ugettext_lazy('limit 4 weeks default 3 weeks')}

    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        
        if data < datetime.date.today():
            return ValidationError(ugettext_lazy('Invalid date - renewal in past'))

        if data > datetime.today.today() + datetime.timedelta(weeks=4):
            return ValidationError(ugettext_lazy('Invalid date - renewal more than 4 weeks ahead'))

        return data

