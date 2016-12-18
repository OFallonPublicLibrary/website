from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms

from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


@login_required
def profile_view(request):
    return render(request, 'core/profile_view.html', {
        'title': 'Account',
        'breadcrumbs': [
            {'name':'Dashboard', 'url_name':'dashboard:dashboard_home'},
            {'name':'Account', 'url_name':'cake'},
        ]
    })

@login_required
def profile_update(request):
    user = request.user
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        user.save()
        return redirect('profile:profile_view')
    return render(request, 'core/profile_update.html', {
        'title': 'Account Update',
        'form': form,
        'breadcrumbs': [
            {'name':'Dashboard', 'url_name':'dashboard:dashboard_home'},
            {'name':'Account', 'url_name':'cake'},
        ]
    })

