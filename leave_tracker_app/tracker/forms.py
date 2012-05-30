from django.forms import ModelForm 
from models import LeaveApplication

class LeaveApplicationForm(ModelForm):
    
    class Meta:
        model = LeaveApplication
        exclude = ('status')


