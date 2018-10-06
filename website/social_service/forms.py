from django import forms
from social_service.models import Claim, Period
from accounts.models import Student, Document


class FirstStepForm(forms.ModelForm):
	class Meta:
		model = Period
		fields = ['application_type']
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['application_type'].widget.attrs.update({'class' : 'form-control', 'id' : "select"})


class SecondStepForm(forms.ModelForm):
	class Meta:
		abstract = True
		model = Claim
		fields = ['period', 'documents']
		bool_fields = []

	def __init__(self, student, application_type, *args, **kwargs):
		super(SecondStepForm, self).__init__(*args, **kwargs)
		self.fields['period'].queryset = Period.objects.filter(application_type = application_type) 
		self.fields['period'].widget.attrs.update({'class' : 'form-control', 'id' : "select"})
		self.fields['documents'].queryset = Document.objects.filter(student = student)
		self.fields['documents'].widget.attrs.update({'name' : "multiple-select", 'id' : "multiple-select", 'multiple' : "", 'class' : "form-control"})
		self.fields['additional_information'].widget.attrs.update({"class" : "form-control"})			
		self.fields['canteen_preference'].widget.attrs.update({'class' : 'form-control', 'id' : "select"})
		for field in self.Meta.bool_fields : 
			self.fields[field].widget.attrs.update({"class" : "form-check-input"})

	def clean(self):
		cd = self.cleaned_data

		if len(self.Meta.bool_fields) > 0 :
			bools_checked = False
			for field in self.Meta.bool_fields : bools_checked = bools_checked or cd.get(field)
		else : 
			bools_checked = True

		if not bools_checked :
			raise forms.ValidationError("Вы должны выбрать одну из причин для получения помощи")
		
		return cd


class AposSingleForm(SecondStepForm):

	class Meta(SecondStepForm.Meta):
		bool_fields = [
			'lives_in_dormitory',
			'has_no_scholarship'
		]
		fields = SecondStepForm.Meta.fields + bool_fields


class AposRegularForm(SecondStepForm):

	class Meta(SecondStepForm.Meta):
		bool_fields = [
			'is_orphan',
			'is_one_of_many_children',
			'parents_are_disabled',
			'from_incomlete_family',
			'has_chronic_illness',
			'is_disabled',
			'has_children',
			'is_participant_of_hostilities',
			'lives_in_dormitory',
			'affected_by_chernobyl'
		]
		fields = SecondStepForm.Meta.fields + bool_fields


class MealsForm(SecondStepForm):

	class Meta(SecondStepForm.Meta):
		bool_fields = [
			'is_orphan',
			'is_one_of_many_children',
			'parents_are_disabled',
			'from_incomlete_family',
			'has_chronic_illness',
			'from_poor_family',
			'is_in_severe_conditions'
		]
		fields = SecondStepForm.Meta.fields + bool_fields + \
			['additional_information', 'canteen_preference']


class ProfilaktoryForm(SecondStepForm):

	class Meta(SecondStepForm.Meta):
		bool_fields = []
		fields = SecondStepForm.Meta.fields + bool_fields
