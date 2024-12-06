from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView
from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from . import forms

def is_user_admin(user):
    admin_group = Group.objects.get(name="Administrator") 
    return admin_group.user_set.filter(username=user).exists()


@login_required
def index(request):
    return render(request, 'main/index.html')


# gets all users who are not admins
class UsersList(UserPassesTestMixin, ListView):
    template_name = 'admin/users_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name="Administrator").exists()

    def get_queryset(self):
        return User.objects.filter(groups__name='Korisnik')


@user_passes_test(is_user_admin)
def createUser(request):
    if request.method == 'POST':
        form = forms.AddUserForm(request.POST)

        # if this is a POST request we need to process the form data
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = forms.AddUserForm(request.POST)

            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                user_name = form.cleaned_data['user_name']  # Use the cleaned data

                if User.objects.filter(username=user_name).exists():
                    # user already exists
                    form.add_error(None, 'Navedeno korisničko ime već postoji!')
                else:
                    # create new user
                    new_user = User.objects.create_user(
                        username=user_name,
                        password=form.cleaned_data['user_password']
                    )
                    
                    group = Group.objects.get(name="Korisnik")
                    new_user.groups.add(group)

                    # add a success message
                    messages.success(request, 'Korisnik "{}" je supješno kreiran!'.format(user_name))
                    return HttpResponseRedirect("/adminDashboard")
    else:
        form = forms.AddUserForm()
    
    return render(request, 'admin/create_user.html', {'form': form})
