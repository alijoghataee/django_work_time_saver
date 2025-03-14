from django import forms
from django.forms import modelformset_factory
from .models import Project, WorkTime


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'hex_color']
        widgets = {
            'hex_color': forms.TextInput(attrs={'type': 'color'})
        }


class WorkTimeForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super(WorkTimeForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['first_name'].initial = user.first_name

    class Meta:
        model = WorkTime
        fields = ['project', 'description', 'start_time', 'end_time', 'worked_minutes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
