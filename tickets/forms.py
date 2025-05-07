from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'w-full border p-2 rounded mb-4', 'placeholder': 'Digite o título'}),
            'descricao': forms.Textarea(attrs={'class': 'w-full border p-2 rounded mb-4', 'placeholder': 'Descreva o problema em detalhes'}),
        }
