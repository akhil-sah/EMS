from django.db import models

# Create your models here.
class Person(models.Model):
	name = models.CharField(max_length = 50)

class Phone_no(models.Model):
	person = models.ForeignKey(Person, on_delete = models.CASCADE)
	phone_no = models.IntegerField()

class Email(models.Model):
	person = models.ForeignKey(Person, on_delete = models.CASCADE)
	email = models.EmailField()

class Complaints(models.Model):
	person = models.ForeignKey(Person, on_delete = models.CASCADE)
	complaint = models.TextField()
	rules_violated = models.TextField()
	status = models.CharField(default = "Relevant", max_length = 15)  #relevant, irrelevant, resolved
	last_update = models.DateField(auto_now = True)  

class Emission_parameters(models.Model):
	substance_name = models.CharField(max_length = 50)
	substance_type = models.CharField(max_length = 50)
	permissible_limit = models.IntegerField()
	unit = models.CharField(max_length = 20)
	relation = models.CharField(default = "max", max_length = 10)   #maximum\minimum permissible limit

class Survey_metadata(models.Model):    # all surveys will be displayed in a table and to see details of survey we will click on link (like trip_planner)
	auditor = models.ForeignKey(Person, on_delete = models.CASCADE)
	date = models.DateField()
	population = models.IntegerField()
	num_issues = models.IntegerField()   #number of issues
	relevant_issues = models.IntegerField()
	resolved_issues = models.IntegerField(default = 0)  #will be updated while writing the survey report

class Survey_data(models.Model):  
	surveyor = models.ForeignKey(Person, on_delete = models.CASCADE) 
	person = models.CharField(max_length = 50)
	servey_id = models.ForeignKey(Survey_metadata, on_delete = models.CASCADE)
	feedback = models.TextField()
	status = models.CharField(max_length = 20)   # the problem (if any addressed or not)
	last_date = models.DateField(auto_now = True) #

class Session(models.Model):
	supervisor = models.ForeignKey(Person, on_delete = models.CASCADE)
	date = models.DateField()


class Company_emissions(models.Model):
	session = models.ManyToManyField(Session)
	substance = models.ForeignKey(Emission_parameters, on_delete = models.CASCADE)
	value = models.IntegerField()
	
