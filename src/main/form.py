from django import forms
from django.contrib.auth.models import User
from main.models import Student, Group


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )

class AddStudentForm(forms.ModelForm):
    birthdate = forms.DateField(required=False)
    class Meta:
        model = Student
        exclude = (
            'image',
            'birthdate',
        )

class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group