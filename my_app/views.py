from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate,login
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def index_view(request, *args, **kwargs):
	print(request)
#	obj = Person.objects.get(condition)
#	return HttpResponse("<h1>Hello World</h>")
	return render(request, "index.html", {})

#def permissible_emissions_view(request, *args, **kwargs):
#	obj = Emission_parameters.object.get

def login_view(request):
	if request.method == 'POST':
		form = login_form(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request,username = cd['username'], password = cd['password'])

			if user is not None:
				if user.is_active:
					login(request,user)
					person = Person.objects.get(user = user)
					print(person.role)
					return render(request,'home.html',{'user':user, 'person':person})

				else:
					return HttpResponse("Disabled Account")

			else:
				form = login_form()
				return render(request,'invalidLogin.html',{'form':form})

	else:
		form = login_form()

	return render(request,'login.html',{'form':form})

def register_view(request):
	if request.method == 'POST':
		user_form = user_registration_form(request.POST)
		if user_form.is_valid():
			#Create new user object....dont save now
			new_user = user_form.save(commit = False)
			#Set chosen Password
			new_user.set_password(user_form.cleaned_data['password'])
			#Save the user object
			new_user.save()
			person = Person.objects.create(user = new_user)
			person.save()
			return render(request,'registered.html',{'new_user':new_user})
	else:
		user_form = user_registration_form()
	return render(request, 'register.html', {'user_form':user_form})


@login_required
def edit_view(request):
	if request.method == 'POST':
		user_form = user_edit_form(instance = request.user,data = request.POST)
		
		if user_form.is_valid():
			user_form.save()

			user = request.user
			return render(request,'index.html',{'user':user})

	else:
		user_form = user_edit_form(instance = request.user)

	return render(request,'profile.html', {'user_form':user_form}) #on page where info is visible make it updateable

@login_required
def home_view(request):
	user = request.user
	person = Person.objects.get(user = user)
	print(person.role)
	return render(request,'home.html',{'user':user,'person':person})      #->Work this out.



"""
@login_required
def survey_data_view(request):
	user = request.user
	surveyor = Person.objects.get(user = user)
	try:
		serveys = Servey_data.objects.filter(survey_id = surveyor, draft = True).order_by('-pub_date')
	except:
		userDrafts = None
	return render(request,'blog/userDrafts.html',{'userDrafts':userDrafts})
"""