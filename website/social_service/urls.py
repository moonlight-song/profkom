from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'new/$', views.FirstStepFormView.as_view()),
    url(r'new/(?P<application_type>[-\w]+)/$', views.SecondStepFormView.as_view()),
]