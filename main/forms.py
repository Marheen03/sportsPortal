from django import forms

class AddUserForm(forms.Form):
    user_name = forms.CharField(label="Korisničko ime: ", max_length=20)
    user_password = forms.CharField(label="Lozinka: ", max_length=20)