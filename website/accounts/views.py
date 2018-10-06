from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView as DjangoAuthLoginView
from django.views import View
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect

from website import settings
from accounts.models import Student
from social_service.models import Claim
from .forms import ProfileForm

class StudentStatusRequiredMixin(object):

	def dispatch(self, request, *args, **kwargs):

		print (request.GET)
		print (self.args)
		print (self.kwargs)


		if request.user.is_authenticated():
			print ('authenticated')
			if request.user.groups.filter(name = settings.GROUP_STUDENTS) :	
				return super(StudentStatusRequiredMixin, self).dispatch(request, *args, **kwargs)
			else :
				request.session['error_message'] = 'У Вас недостаточно прав доступа к этой странице! \
					Для просмотра страницы войдите как студент'
				return redirect ('/account/login?next=' + request.path)
		else :
			print ('Not authenticated')
			return redirect ('/account/login?next=' + request.path)
	

class IndexView(StudentStatusRequiredMixin, View):
	template_name = 'account/index.html'

	def get(self, request, *args, **kwargs):

		student = request.user.student
		claims = Claim.objects.filter(student = student)

		STATUS_CSS_CLASSES = {
			'pending' : 'btn-outline-primary',
			'approved' : 'btn-outline-success',
			'rejected' : 'btn-outline-danger',
		}

		css_classes = {
			'status' : [],
		}
		for claim in claims : 
			css_classes['status'].append(STATUS_CSS_CLASSES[claim.status])

		return render(request, self.template_name, {'claims': claims, 'css_classes' : css_classes})


class ProfileView (StudentStatusRequiredMixin, UpdateView) :
	model = Student
	form_class = ProfileForm

	template_name = 'account/profile.html'


	def get_object (self, *args, **kwargs) :
		return self.request.user.student
