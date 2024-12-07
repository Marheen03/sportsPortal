from django.shortcuts import redirect, render
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


# gets all users
class UsersList(UserPassesTestMixin, ListView):
    template_name = 'admin/users_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name="Administrator").exists()

    def get_queryset(self):
        return User.objects.all()


@user_passes_test(is_user_admin)
def createUser(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.UserFormCreate(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user_name = form.cleaned_data['username']

            # create new user
            new_user = User.objects.create_user(
                username=user_name,
                password=form.cleaned_data['password']
            )
                    
            user_type = form.cleaned_data['vrsta_korisnika']
            group = Group.objects.get(name=user_type)
            new_user.groups.add(group)

            # add a success message
            messages.success(request, 'Korisnik "{}" je uspješno kreiran!'.format(user_name))
            return HttpResponseRedirect("/adminDashboard")
    else:
        form = forms.UserFormCreate()
    
    return render(request, 'admin/user_form.html', {'form': form, 'form_action': 'create'})


@user_passes_test(is_user_admin)
def editUser(request, userID):
    user = User.objects.get(id=userID)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.UserFormEdit(request.POST, instance=user)

        if form.is_valid():
            user_name = form.cleaned_data['username']
            form.save()

            # add a success message
            messages.success(request, 'Korisnik "{}" je uspješno ažuriran!'.format(user_name))
            return HttpResponseRedirect("/adminDashboard")
    else:
        # populate the form with the chosen user's data
        form = forms.UserFormEdit(instance=user)
    
    return render(request, 'admin/user_form.html', {'form': form, 'form_action': 'edit', 'userID': user.id})


@user_passes_test(is_user_admin)
def deleteUser(request, userID):
    user = User.objects.get(id=userID)
    try:
        user.delete()
        messages.success(request, 'Korisnik "{}" je supješno obrisan!'.format(user.username))
        return redirect('usersList')
    except User.DoesNotExist:
        return redirect('usersList')
