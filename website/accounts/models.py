from django.db import models
from django.contrib.auth.models import User 


class Department (models.Model):

	name = models.CharField (max_length = 20, unique = True) 

	def __str__ (self) :
		return self.name
    	

class Student (models.Model) :

	user = models.OneToOneField (
		User, 
		on_delete = models.CASCADE
	)
	department = models.ForeignKey (
		Department, 
		verbose_name = 'Факультет',
		blank = True,
		null = True, 
		on_delete = models.SET(None)
	)


	academic_group = models.CharField (
		verbose_name = 'Академическая группа',
		max_length = 20, 
		)
	dormitory_building = models.CharField (
		verbose_name = 'Общежитие (корпус)',
		max_length = 20, 
		blank = True
		)
	dormitory_room = models.CharField (
		verbose_name = 'Общежитие (комната)',
		max_length = 20, 
		blank = True
		)
	scholarship = models.PositiveIntegerField (
		verbose_name = 'Стипендия',
		default = 0
		)
	phone = models.CharField (
		verbose_name = 'Телефон',
		max_length = 30, 
		blank = True
		)
	vk = models.CharField (
		verbose_name = 'Ссылка на страницу ВК',
		max_length = 30, 
		blank = True
		)


	def __str__ (self) :
		return '{} ({})'.format (self.user.get_full_name(), self.department)

	def lives_in_dorm (self) : 
		return bool(self.dormitory_building)

	def receives_scholarship (self) :
		return bool(self.scholarship)



def get_user_directory_path(instance, filename):
	return 'user_{0}/{1}'.format(instance.student.id, filename)

class Document (models.Model):

	name = models.CharField (max_length = 128)
	
	student = models.ForeignKey (
		Student,  
		on_delete = models.CASCADE)

	file = models.FileField (upload_to = get_user_directory_path)

	def __str__ (self) :
		return self.name


class Proforg (models.Model):

	user = models.OneToOneField (User, on_delete = models.CASCADE)
	department = models.ForeignKey (Department, blank = True, on_delete = models.SET(''))

	def __str__ (self) :
		return self.user.username