from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
 
# Create your views here.
def index_view(request, *args, **kwargs):
	return render(request, "index.html", {})

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
					# print(person.role)
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

def password_reset_view(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			print(associated_users)
			if associated_users.exists():
				print(2)
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password-reset/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password-reset/done/")
	password_reset_form = PasswordResetForm()
	print('here')
	return render(request=request, template_name="password-reset/password_reset_form.html", context={"password_reset_form":password_reset_form})

@login_required
def edit_view(request):
	person = Person.objects.get(user = request.user)
	try:
		phone_no = Phone_no.objects.get(person = person)
	except:
		phone_no = int()
	if request.method == 'POST':
		user_data = {
			'first_name': request.POST['first_name'],
			'last_name': request.POST['last_name'],
			'email': request.POST['email']
		}

		contact_data = {
			'phone_no': request.POST['phone_no']
		}

		user_form = user_edit_form(instance = request.user,data = user_data)
		contact_form = contact_edit_form(instance = request.user,data = contact_data)

		if user_form.is_valid() and contact_form.is_valid():
			con_cln = contact_form.cleaned_data
			phone_no = Phone_no(person = person, phone_no = con_cln['phone_no'])
			phone_no.save()

			user_form.save()

		return render(request,'profile.html',{'person': person, 'phone_no':phone_no})

	else:
		user_form = user_edit_form(instance = request.user)
		contact_form = contact_edit_form(instance = request.user)
	
	return render(request,'profile.html',{'person': person, 'phone_no':phone_no})

@login_required
def password_change_done_view(request):
	person = Person.objects.get(user = request.user)
	return render(request,'password_change_done.html', {'person': person})

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
def select_session_page(request):
	context = {"sessions": Session.objects.filter(supervisor=Person.objects.get(user=request.user))}
	print(context["sessions"])
	if request.method == 'POST':
		user_form = enter_session_form(instance = request.user, data = request.POST)
		if user_form.is_valid():
			user = request.user
			person = Person.objects.get(user = user)
			cd = user_form.cleaned_data
			attr= cd['session']
			context.update({'user': user})
	else:
		# Why this form is passed ?
		user_form = user_edit_form(instance = request.user)
		context.update({'user_form': user_form})
	return render(request,'select_session.html', context)

@login_required
def enter_emissions(request):
	'''
	# NOTE: In this project we pull the list every time new attribute is entered
	and list of left attributes is pulled from server.
	Better version is to do all this on client side and support multiple pulls
	at same time.
	# NOTE: Only one supervisor should be able to edit the emissions else there
	is high chance of inconsistancies.
	'''
	id=1
	filled = Company_emissions.objects.filter(session=id)
	attributes_filled = list()
	for attr in filled:
		attributes_filled.append(attr.substance.substance_name)
	lefts = Emission_parameters.objects.all()
	attributes_left = list()
	for attr in lefts:
		if attr.substance_name in attributes_filled:
			continue
		attributes_left.append(attr)
	context = {
		"attributes_left": attributes_left,
		"attributes_filled": filled,
	}
	if request.method == 'POST':
		user_form = enter_emissions_form(instance = request.user, data = request.POST)
		if user_form.is_valid():
			user = request.user
			person = Person.objects.get(user = user)
			cd = user_form.cleaned_data
			attr= cd['substance']
			value = cd['value']
			context.update({'user': user})
	else:
		user_form = user_edit_form(instance = request.user)
		context.update({'user_form': user_form})
	return render(request,'emissions.html', context)
 

@login_required
def track_complaint_view(request):
	user = request.user
	person = Person.objects.get(user = user)
	complaints = Complaints.objects.filter(person = person).order_by('-last_update')
	return render(request,'track_complaint.html',{'complaints':complaints})

@login_required
def audit_complaints_view(request):
	complaints = Complaints.objects.all().order_by('-last_update')
	return render(request,'audit_complaints.html',{'complaints':complaints})

@login_required
def complaint_feedback_view(request, complaint_id):
	complaint = Complaints.objects.get(id = complaint_id)
	if request.method == 'POST':
		complaint.feedback = request.POST['feedback']
		complaint.status = request.POST['status']
		complaint.save()
		
		subject = 'Complaint Status update'
		message = f"""Hi {complaint.person.user.first_name} {complaint.person.user.last_name}. 
		Thank you for bringing our attention to problem (mentioned by you in complaint no {complaint.id}.
		After reviewing the facts provided by the response of our team is given below.
		{complaint.feedback}"""
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [complaint.person.user.email, ]
		send_mail( subject, message, email_from, recipient_list )
		
		return redirect('audit_complaints')
		#add email part
	return render(request,'complaint_feedback.html',{'complaint':complaint})

@login_required
def audit_surveys_view(request):
	surveys = Survey_metadata.objects.all().order_by('-date')
	return render(request,'audit_surveys.html',{'surveys':surveys})

@login_required
def survey_response_view(request, survey_id, response_id = 0):
	survey = Survey_metadata.objects.get(id = survey_id)
	responses = Survey_data.objects.filter(survey_id = survey)
	if request.method == 'POST':
		print(request.POST)
		response = Survey_data.objects.get(id = response_id)
		response.status = request.POST['status'] #add button that changes value attribute of status input
		if response.status == "Not addressed":
			pass
		elif response.status == "Addressed":
			survey.num_issues -= 1
			survey.resolved_issues += 1
		elif response.status == "Irrelevant":
			survey.num_issues -= 1
			survey.relevant_issues -= 1
			survey.resolved_issues += 1
		else:
			return HttpResponse("Unidentified status")
		response.save()
		survey.save()

	return render(request,'survey_response.html',{'responses':responses, 'survey_id':survey_id})	

@login_required
def audit_emissions_view(request):
	company_emissions = Company_emissions.objects.all().order_by('-session__date', 'substance__substance_name')
	session_sub = dict()
	session_dt = dict()
	for company_emission in company_emissions:
		print(company_emission.substance.substance_name)
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
	pers = Person.objects.get(user = request.user)
	if request.method == 'POST':
		#print(request.)
		user = User.objects.get(email = request.POST['auditor'])
		person = Person.objects.get(user = user)
		if person.role != "Auditor":
			print("Not auditor")
			return render(request,'new_survey.html', {'user_form':user_form, 'pers':pers})
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
			return render(request,'survey_created.html',{'obj':obj, 'pers':pers})

	else:
		user_form = new_survey_form(instance = request.user)

	return render(request,'new_survey.html', {'user_form':user_form, 'pers':pers})

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
			survey.num_issues += 1
			survey.relevant_issues += 1
			survey.save()


			obj = Survey_data(surveyor = person, person = pers, feedback = feedback, survey_id = survey)
			obj.save()
			return render(request,'survey_complete.html',{})

	else:
		user_form = survey_form_form(instance = request.user)

	return render(request,'survey_form.html', {'user_form':user_form, 'survey_id':survey_id})

@login_required
def select_session_page(request):
	context = {"sessions": Session.objects.filter(supervisor=Person.objects.get(user=request.user))}
	print(context["sessions"])
	if request.method == 'POST':
		user_form = enter_session_form(instance = request.user, data = request.POST)
		if user_form.is_valid():
			user = request.user
			person = Person.objects.get(user = user)
			cd = user_form.cleaned_data
			attr= cd['session']
			context.update({'user': user})
	else:
		user_form = enter_session_form(instance = request.user)
		context.update({'user_form': user_form})
	return render(request,'select_session.html', context)

@login_required
def enter_emissions(request):
	'''
	# NOTE: In this project we pull the list every time new attribute is entered
	and list of left attributes is pulled from server.
	Better version is to do all this on client side and support multiple pulls
	at same time.
	# NOTE: Only one supervisor should be able to edit the emissions else there
	is high chance of inconsistancies.
	'''
	id=1
	filled = Company_emissions.objects.filter(session=id)
	attributes_filled = list()
	for attr in filled:
		attributes_filled.append(attr.substance.substance_name)
	lefts = Emission_parameters.objects.all()
	attributes_left = list()
	for attr in lefts:
		if attr.substance_name in attributes_filled:
			continue
		attributes_left.append(attr)
	context = {
		"attributes_left": attributes_left,
		"attributes_filled": filled,
	}
	if request.method == 'POST':
		user_form = enter_emissions_form(instance = request.user, data = request.POST)
		if user_form.is_valid():
			user = request.user
			person = Person.objects.get(user = user)
			cd = user_form.cleaned_data
			attr= cd['substance']
			value = cd['value']
			context.update({'user': user})
	else:
		user_form = user_edit_form(instance = request.user)
		context.update({'user_form': user_form})
	return render(request,'emissions.html', context)

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
