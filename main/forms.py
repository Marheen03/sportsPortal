from django import forms
from django.contrib.auth.models import User
from .models import *

USER_TYPES = {
    "Administrator": "Administrator",
    "Korisnik": "Korisnik"
}

class UserFormCreate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Korisničko ime',
            'password': 'Lozinka'
        }
        help_texts = {
            'username': None
        }
    
    vrsta_korisnika = forms.ChoiceField(choices=USER_TYPES)

class UserFormEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Korisničko ime',
            'password': 'Lozinka'
        }
        help_texts = {
            'username': None
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'team_stadium', 'team_country']
        labels = {
            'team_name': 'Naziv momčadi',
            'team_stadium': 'Naziv stadiona',
            'team_country': 'Država'
        }

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['competition_name', 'competition_country']
        labels = {
            'competition_name': 'Naziv natjecanja',
            'competition_country': 'Država'
        }
    
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Momčadi'
    )
