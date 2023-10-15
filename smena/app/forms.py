from django import forms
from .models import Table, Worker

class TableForm(forms.ModelForm):

    class Meta:
        model = Table
        fields = ('name', 'date')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class WorkerForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = ('fio', )
    
    def is_valid(self) -> bool:
        if not self.cleaned_data.get('fio'):
            self.add_error('fio', "Поле 'Инициалы' обязательно для заполнения")
            
        return super().is_valid()