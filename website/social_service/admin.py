from django.contrib import admin
from .models import Claim, Period
from website import settings


admin.site.register(Period)

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):

	def get_queryset(self, request):
		queryset = super(ClaimAdmin, self).get_queryset(request)

		if request.user.groups.filter(name = settings.GROUP_STAFF) \
		or request.user.is_superuser :
			return queryset

		if request.user.groups.filter(name = settings.GROUP_PROFORGS) :
			return queryset.filter(student__department = request.user.proforg.department)