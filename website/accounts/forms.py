from django import forms
from accounts.models import Student


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = [
			'department',
			'academic_group',
			'dormitory_building',
			'dormitory_room',
			'scholarship',
			'phone',
			'vk'
		]

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		for field in self.Meta.fields : 
			self.fields[field].widget.attrs.update({"class" : "form-control"})
		self.fields['department'].widget.attrs.update({'class' : 'form-control', 'id' : "select"})
