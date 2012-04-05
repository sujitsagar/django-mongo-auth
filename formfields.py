import datetime

from django import forms

class FormLimitedDateTimeField(forms.DateTimeField):
    def __init__(self, upper_limit=None, lower_limit=None, input_formats=None, *args, **kwargs):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        if self.upper_limit and not isinstance(self.upper_limit, (datetime.datetime, datetime.date)):
            self.error(u'Invalid upper_limit argument.')
        if self.lower_limit and not isinstance(self.lower_limit, (datetime.datetime, datetime.date)):
            self.error(u'Invalid lower_limit argument.')

        super(FormLimitedDateTimeField, self).__init__(input_formats=None, *args, **kwargs)
   
    def clean(self, value):
        super(FormLimitedDateTimeField, self).clean(value)
        
        try:
            birthdate = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            birthdate = datetime.datetime.strptime(value, '%Y-%m-%d')
            
        
        if self.upper_limit:
            tmp_value = birthdate
            tmp_upper_limit = self.upper_limit
            if not isinstance(birthdate, datetime.datetime) or not isinstance(self.upper_limit, datetime.datetime):
                if isinstance(self.upper_limit, datetime.datetime):
                    tmp_upper_limit = self.upper_limit.date()
                elif isinstance(tmp_value, datetime.datetime):
                    tmp_value = birthdate.date()
            if tmp_value > tmp_upper_limit:
                self.error(u'Value is out of bounds.')
                    
        if self.lower_limit:
            tmp_value = birthdate
            tmp_lower_limit = self.lower_limit
            if not isinstance(birthdate, datetime.datetime) or not isinstance(self.lower_limit, datetime.datetime):
                if isinstance(self.lower_limit, datetime.datetime):
                    tmp_lower_limit = self.lower_limit.date()
                elif isinstance(tmp_value, datetime.datetime):
                    tmp_value = birthdate.date()
            if tmp_value < tmp_lower_limit:
                self.error(u'Value is out of bounds.')