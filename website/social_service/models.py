from django.db import models
from accounts.models import Student, Document
from django.contrib.auth.models import User 


APPLICATION_TYPES = {
	'meals' : 'Бесплатное питание',
	'profilaktory' : 'Профилакторий',
	'apos_regular' : 'Ежемесячный АПОС',
	'apos_single' : 'Единоразовый АПОС'
}

APPLICATION_TYPES_LIST = ['meals', 'profilaktory', 'apos_regular', 'apos_single']

class Period (models.Model) :

	#APPLICATION_TYPE_CHOICES = tuple([(item, item) for item in APPLICATION_TYPES])

	name = models.CharField (max_length = 40)

	application_type = models.CharField(
		max_length = 30,
		choices = tuple([(item, APPLICATION_TYPES[item]) for item in APPLICATION_TYPES_LIST])
	)

	application_start = models.DateField()
	application_end = models.DateField()
	period_start = models.DateField()
	period_end = models.DateField()

	def __str__ (self) : 
		return '{}, {}'.format(self.application_type, self.name)


class Claim (models.Model) :

	# Common properties

	student = models.ForeignKey(
		Student,
		on_delete = models.CASCADE,
	)

	period = models.ForeignKey(
		Period,
		on_delete = models.CASCADE,
	)

	status = models.CharField(
		max_length = 16,
		choices = (
			('pending', 'На рассмотрении'),
			('approved', 'Одобрена'),
			('rejected', 'На рассмотрении'),
		), 
		default = 'pending'
	)

	status_assigned_by = models.ForeignKey(
		User,
		blank = True,
		null = True,
		on_delete = models.SET_NULL,
	)

	status_reason = models.CharField (
		max_length = 256, 
		blank = True,
		default = ''
	)

	sms_notification = models.BooleanField (
		verbose_name = '',
		default = False
	)

	is_orphan = models.BooleanField (
		verbose_name = 'Сирота',
		default = False
	)
	is_one_of_many_children = models.BooleanField (
		verbose_name = 'Из многодетной семьи',
		default = False
	)
	parents_are_disabled = models.BooleanField (
		verbose_name = 'Родители-инвалиды (или пенсионеры)',
		default = False
	)
	from_incomlete_family = models.BooleanField (
		verbose_name = 'Из неполной семьи',
		default = False
	)
	has_chronic_illness = models.BooleanField (
		verbose_name = 'Нахожусь на диспансерном учете с хроническим заболеванием',
		default = False
	)
	is_disabled = models.BooleanField (
		verbose_name = 'Инвалид',
		default = False
	)
	has_children = models.BooleanField (
		verbose_name = 'Есть дети',
		default = False
	)
	is_participant_of_hostilities = models.BooleanField (
		verbose_name = 'Участник боевых действий',
		default = False
	)
	lives_in_dormitory = models.BooleanField (
		verbose_name = 'Проживаю в общежитии',
		default = False
	)
	affected_by_chernobyl = models.BooleanField (
		verbose_name = 'Чернобылец',
		default = False
	)
	has_no_scholarship = models.BooleanField (
		verbose_name = 'Нет стипендии',
		default = False
	)
	from_poor_family = models.BooleanField (
		verbose_name = 'Из неблагополучной семьи',
		default = False
	)
	is_in_severe_conditions = models.BooleanField (
		verbose_name = 'Тяжелое материальное положение',
		default = False
	)
	
	additional_information = models.CharField (
		verbose_name = 'Примечания',
		max_length = 256, 
		blank = True,
		default = ''
	)

	canteen_preference = models.CharField(
		max_length = 8,
		choices = (
			('3rd', 'Столовая 3-ки'),
			('kpm', 'Столовая КПМ'),
			('equal', 'Без разницы'),
		), 
		default = 'equal'
	)
	
	documents = models.ManyToManyField (
		Document,
		blank = True
	)


	def __str__ (self) :
		return '{} : {}'.format (self.student, self.period)

