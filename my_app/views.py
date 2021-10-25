from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser

# Create your views here.
def index_view(request, *args, **kwargs):
#	print(request)
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

@login_required
def logout_view(request):
	logout(request)
	return redirect('index')

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


"""
@login_required
def edit_view(request):
	if request.method == 'POST':
		user_form = user_edit_form(instance = request.user,data = request.POST)

		if user_form.is_valid():
			user_form.save()

			user = request.user
			return render(request,'home.html',{'user':user})

	else:
		user_form = user_edit_form(instance = request.user)
 
	return render(request,'profile.html', {'user_form':user_form}) #on page where info is visible make it updateable
"""
"""
@login_required
def edit_view(request):
	person = Person.objects.get(user = request.user)

	if request.method == 'POST':
		user_form = user_edit_form(instance = request.user,data = request.POST)
		profile_form = profile_edit_form(instance = person,data = request.POST, files = request.FILES)
		contact_form = contact_edit_form(instance = person,data = request.POST, files = request.FILES)

		if user_form.is_valid() and profile_form.is_valid() and contact_form.is_valid():
			user_form.save()
			profile_form.save()
			contact_form.save()

			return render(request,'home.html',{'user':user,'person':person})

	else:
		user_form = user_edit_form(instance = request.user)
		profile_form = profile_edit_form(instance = person)
		contact_form = contact_edit_form(instance = person)

	return render(request,'profile.html',{'user': request.user, 'person': person, 'user_form':user_form,
		                                  'profile_form':profile_form, 'contact_form': contact_form})
"""
@login_required
def home_view(request):
	user = request.user
	person = Person.objects.get(user = user)
#	print(person.role)
	return render(request,'home.html',{'user':user,'person':person})      #->Work this out.
 

def permissible_emissions_view(request):
	emissions = Emission_parameters.objects.all()
	if isinstance(request.user, AnonymousUser):
		person = Person()
	else:
		person = Person.objects.get(user = request.user)
	return render(request, 'permissible_emissions.html', {'emissions':emissions, 'person':person})


@login_required
def profile_view(request):
	user = request.user
	person = Person.objects.get(user = user)
	return render(request, 'profile.html', {'user':user, 'person': person})

@login_required
def lodge_complaint_view(request):
	if request.method == 'POST':
		user_form = lodge_complaint_form(instance = request.user, data = request.POST)

		if user_form.is_valid():
			user = request.user
			person = Person.objects.get(user = user)

			cd = user_form.cleaned_data
			complaint = cd['complaint']
			rules_violated = cd['rules_violated']
 
			obj = Complaints(person = person, complaint = complaint, rules_violated = rules_violated)
			obj.save()
			return render(request,'complaint_lodged.html',{'user':user, 'complaint':obj})

	else:
		user_form = lodge_complaint_form(instance = request.user)

	return render(request,'lodge_complaint.html', {'user_form':user_form})

@login_required
def enter_emissions(request):
	context = {
		"attributes_left": ["CO2", "NH3", "CH4"],
		"attributes_filled": {"H2O": 10, "SO2": 20, "H2S": 30},
	}
	return render(request,'emissions.html', context)
 

@login_required
def track_complaint_view(request):
	user = request.user
	person = Person.objects.get(user = user)
	complaints = Complaints.objects.filter(person = person).order_by('last_update')
	return render(request,'track_complaint.html',{'complaints':complaints})
"""
@login_required
def track_complaint2_view(request, complaint_id):
	complaint = get_object_or_404(Complaints, pk = complaint_id)
	return render(request,'track_complaint.html',{'complaint':complaint})
"""
""" 
@login_required
def audit_complaints_view(request):
	#add a feedback column for each complaint (not visible to complainer)
	#this will be edited by auditor and a mail with feedback sent to complainer
	complaints = Complaints.objects.all().order_by('last_update')
	return render(request,'audit_complaints.html',{'complaints':complaints})
"""
@login_required
def audit_complaints_view(request, complaint_id):
	#add a feedback column for each complaint (not visible to complainer)
	#this will be edited by auditor and a mail with feedback sent to complainer
	print(complaint_id)
	complaints = Complaints.objects.all().order_by('last_update')
	if request.method == "POST":
		complaint = Complaints.objects.get(id = complaint_id)
		complaint.feedback = request.POST['feedback']
		complaint.status = request.POST['status']
		complaint.save()
	print('rendered')
	return render(request,'audit_complaints.html',{'complaints':complaints})


@login_required
def audit_surveys_view(request):
	sessions = Session.objects.all().order_by('date')
	return render(request,'audit_surveys.html',{'sessions':sessions})
	

@login_required
def audit_emissions_view(request):
	company_emissions = Company_emissions.objects.all().order_by('-session__date', 'substance__substance_name')
	session_sub = dict()
	session_dt = dict()
	for company_emission in company_emissions:
		if session_sub[company_emission.session.id] is None:
			session_sub[company_emission.session.id] = [(company_emission.substance.substance_name, company_emission.value,
			                                            Emission_parameters.objects.get(substance_name = company_emission.substance.substance_name).min_permissible_limit,
														Emission_parameters.objects.get(substance_name = company_emission.substance.substance_name).max_permissible_limit)]
			session_dt[company_emission.session.id] = [company_emission.session.date]
		else:
			session_sub[company_emission.session.id].append((company_emission.substance, company_emission.value,
															Emission_parameters.objects.get(substance_name = company_emission.substance.substance_name).min_permissible_limit,
															Emission_parameters.objects.get(substance_name = company_emission.substance.substance_name).max_permissible_limit))			
	return render(request,'audit_emissions.html',{'session_sub':session_sub, 'session_dt': session_dt})

@login_required
def surveys_view(request):
	surveys = Survey_metadata.objects.all().order_by('-date')
	return render(request, 'surveys.html', {'surveys':surveys})
 
@login_required
def new_survey_view(request):
	#print(request.body)
	if request.method == 'POST':
		#print(request.)
		user = User.objects.get(email = request.POST['auditor'])
		person = Person.objects.get(user = user)
		if person.role != "Auditor":
			print("Not auditor")
			return render(request,'new_survey.html', {'user_form':user_form})
		data = {
		'auditor': person,
		'date': request.POST['date'],
		'population': request.POST['population']		
		}
		print(data['auditor'])
		user_form = new_survey_form(instance = request.user, data = data)
		print(user_form.errors)
		if user_form.is_valid():
			obj = Survey_metadata(auditor = person, date = data['date'], population = data['population'])
			obj.save()
			return render(request,'survey_created.html',{'obj':obj})

	else:
		user_form = new_survey_form(instance = request.user)

	return render(request,'new_survey.html', {'user_form':user_form})


@login_required
def survey_form_view(request, survey_id):
	if request.method == 'POST':
		user_form = survey_form_form(instance = request.user, data = request.POST)
		print(user_form.errors)
		if user_form.is_valid():
			person = Person.objects.get(user = request.user)
			print('1')
			cd = user_form.cleaned_data
			pers = cd['person']
			feedback = cd['feedback']
			
			survey = Survey_metadata.objects.get(id = survey_id)
			survey.population += 1
			survey.num_issues += 1
			survey.relevant_issues += 1


			obj = Survey_data(surveyor = person, person = pers, feedback = feedback, survey_id = survey)
			obj.save()
			return render(request,'survey_complete.html',{})

	else:
		user_form = survey_form_form(instance = request.user)

	return render(request,'survey_form.html', {'user_form':user_form, 'survey_id':survey_id})

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
