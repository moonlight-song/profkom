from django.shortcuts import render, redirect
from django.views import View

from . import forms
from .models import APPLICATION_TYPES, Claim, Period
from accounts.views import StudentStatusRequiredMixin


class FirstStepFormView(StudentStatusRequiredMixin, View):
	template_name = 'social_service/forms/first_step.html'
	url_next = '/account/claims/new/{}/'

	def get(self, request, *args, **kwargs):
		form = forms.FirstStepForm()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = forms.FirstStepForm(request.POST)
		if form.is_valid():
			return redirect (self.url_next.format(request.POST.get("application_type")))
		else :
			return render(request, self.template_name, {'form': form})


class SecondStepFormView(StudentStatusRequiredMixin, View):
	template_name = 'social_service/forms/second_step.html'

	def get(self, request, *args, **kwargs):
		
		form = self.get_form()

		return render(request, self.template_name, {
			'form': form, 
			'form_checkboxes' : self.get_checkboxes(form)
		})


	def post(self, request, *args, **kwargs):
				
		form = self.get_form(request.POST)

		if form.is_valid() :
			Claim.objects.create (form.cleaned_data.update ({'student' : request.user.student}))
			request.session['success_message'] = 'Заявка успешно создана!'
			return redirect ('/account/')
		else :
			return render(request, self.template_name, {
				'form': form, 
				'form_checkboxes' : self.get_checkboxes(form)
			})


	def get_form (self, *args, **kwargs) :

		application_type = self.kwargs['application_type']

		def underscores_to_camel_case(string) :
			result = string.capitalize()
			while result.find('_') > 0 :
				index = result.find('_')
				result = result[:index+1].replace('_', '') + result[index+1:].capitalize()
			return result

		if application_type in APPLICATION_TYPES :
			FormClass = getattr(forms, underscores_to_camel_case(application_type) + 'Form')
			return FormClass (self.request.user.student, application_type, *args, **kwargs)


	def get_checkboxes (self, form) :
		form_checkboxes = []
		if len (form.Meta.bool_fields) > 0:
			for item in form.Meta.bool_fields : 
				form_checkboxes.append (form[item])
		return form_checkboxes
