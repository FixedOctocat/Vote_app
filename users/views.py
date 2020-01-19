from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserRegForm

# Create your views here.
def login_user(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)

			_redirect = request.GET.get('next', 'home')

			return redirect(_redirect)
		else:
			messages.error(request, 'Bad username or password!')

	return render(request, 'users/login.html')

@login_required
def logout_user(request):
	logout(request)
	return redirect('home')

def user_reg(request):
	if request.method == 'POST':
		form = UserRegForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			password1 = form.cleaned_data['password1']
			email = form.cleaned_data['email']
			
			user = User.objects.create_user(username=username, password=password1, email=email)
			
			messages.success(request, 'You account registered, {}!'.format(user.username))

			return redirect('users:login')
		else:
			pass
	else:
		form = UserRegForm()
	
	context = {
		'form':form
	}

	return render(request, 'users/register.html', context)