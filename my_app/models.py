from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now 

# Create your models here.
class Person(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
	role = models.CharField(max_length = 50, default = "viewer")

class Phone_no(models.Model):
	person = models.ForeignKey(Person, on_delete = models.CASCADE)
	phone_no = models.IntegerField()

class Complaints(models.Model):
	person = models.ForeignKey(Person, on_delete = models.CASCADE)
	complaint = models.TextField()
	rules_violated = models.TextField()
	status = models.CharField(default = "Relevant", max_length = 15)  #relevant, irrelevant, resolved
	feedback = models.TextField(default = "None", )
	last_update = models.DateField(auto_now = True)  

class Emission_parameters(models.Model):
	substance_name = models.CharField(max_length = 50)
	substance_type = models.CharField(max_length = 50)
	min_permissible_limit = models.IntegerField(default = 0)
	max_permissible_limit = models.IntegerField()
	unit = models.CharField(max_length = 20)

class Survey_metadata(models.Model):    # all surveys will be displayed in a table and to see details of survey we will click on link (like trip_planner)
	auditor = models.ForeignKey(Person, on_delete = models.CASCADE)
	date = models.DateField()
	population = models.IntegerField(default = 0)
	num_issues = models.IntegerField(default = 0)   #number of issues
	relevant_issues = models.IntegerField(default = 0)
	resolved_issues = models.IntegerField(default = 0)  #will be updated while writing the survey report

class Survey_data(models.Model):
	surveyor = models.ForeignKey(Person, on_delete = models.CASCADE)
	person = models.CharField(max_length = 50)
	survey_id = models.ForeignKey(Survey_metadata, on_delete = models.CASCADE)
	feedback = models.TextField()
	status = models.CharField(max_length = 20, default = "Not addressed")   # the problem (if any addressed or not)
	last_date = models.DateField(auto_now = True) #

class Session(models.Model):
	supervisor = models.ForeignKey(Person, on_delete = models.CASCADE)
	date = models.DateField()

class Company_emissions(models.Model):
	session = models.ForeignKey(Session, on_delete=models.CASCADE)
	substance = models.ForeignKey(Emission_parameters, on_delete = models.CASCADE)
	value = models.IntegerField()
