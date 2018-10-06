from django.contrib import admin
from .models import Student, Department, Proforg, Document
from website import settings


admin.site.register (Department)
admin.site.register (Proforg)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
        
	def get_queryset(self, request):

		queryset = super(StudentAdmin, self).get_queryset(request)

		if request.user.groups.filter(name = settings.GROUP_STAFF) \
		or request.user.is_superuser :
			return queryset

		if request.user.groups.filter(name = settings.GROUP_PROFORGS) :
			return queryset.filter(department = request.user.proforg.department)

admin.site.register (Document)
