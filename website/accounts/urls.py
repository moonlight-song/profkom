from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'$', views.IndexView.as_view(), name = 'index'),
	url(r'^profile/$', views.ProfileView.as_view(success_url="/account/")),
	
	url(r'^claims/', include('social_service.urls')),

	url(r'^login/$', auth_views.LoginView.as_view (
			template_name = 'account/login.html'
		), name = 'login'),
	url(r'^logout/$', auth_views.LogoutView.as_view (
			template_name = 'account/logged_out.html'
		), name = 'logout'),
	url(r'^password_change/$', auth_views.PasswordChangeView.as_view (
			template_name = 'registration/password_change_form.html'
		), name = 'password_change'),
	url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view (
			template_name = 'registration/password_change_done.html'
		), name = 'password_change_done'),
]
