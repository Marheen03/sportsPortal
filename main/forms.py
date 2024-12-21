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
        fields = '__all__'
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

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = '__all__'
        labels = {
            'match_date': 'Datum utakmice',
            'match_stadium': 'Stadion',
            'match_competition': 'Natjecanje',
            'match_team1': 'Momčad 1',
            'match_team2': 'Momčad 2',
            'match_score1': 'Rezultat za 1. momčad',
            'match_score2': 'Rezultat za 2. momčad',
        }
        widgets = {
            'match_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            )
        }
    
    def clean(self):
        cleaned_data = super().clean()
        match_competition = cleaned_data.get('match_competition')
        match_team1 = cleaned_data.get('match_team1')
        match_team2 = cleaned_data.get('match_team2')

        # ensure match_competition is not None
        if not match_competition:
            raise forms.ValidationError("Natjecanje mora biti odabrano.")

        # ensure match_team1 and match_team2 are not None
        if not match_team1 or not match_team2:
            raise forms.ValidationError("Obje momčadi moraju biti odabrane.")

        # ensure match_team1 and match_team2 are different
        if match_team1 == match_team2:
            raise forms.ValidationError("Momčad 1 i Momčad 2 ne mogu biti iste.")

        return cleaned_data
