import os
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import TemplateView, ListView, DetailView, FormView
from main import models
from main.form import RegistrationForm, AddStudentForm, AddGroupForm
from main.models import Student, Group


class IndexView(ListView):
    template_name = 'lists/index.html'
    model = Group
    context_object_name = "group_list"

class StudentView(ListView):
    template_name = 'lists/group.html'
    context_object_name = "students"
    paginate_by = 3

    def get_queryset(self):
        return Student.objects.filter(group=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        context['group'] = Group.objects.get(pk=self.kwargs['pk'])
        return context

class RegistrationView(FormView):
    template_name = 'user/registration.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_invalid(self, form):
        return super(RegistrationView, self).form_invalid(form)

    def form_valid(self, form):
        user = User.objects.create_user(
            form.cleaned_data.get('username'),
            form.cleaned_data.get('email'),
            form.cleaned_data.get('password')
        )
        user.save()
        return super(RegistrationView, self).form_valid(form)

class AddStudentView(FormView):
    template_name = 'manage/manage_student.html'
    form_class = AddStudentForm
    success_url = '/'

    def form_invalid(self, form):
        return super(AddStudentView, self).form_invalid(form)

    def form_valid(self, form):
        student = Student.objects.create(
            fname = form.cleaned_data.get('fname'),
            sname = form.cleaned_data.get('sname'),
            lname = form.cleaned_data.get('lname'),
            ticket = form.cleaned_data.get('ticket'),
            birthdate = form.cleaned_data.get('birthdate'),
            group = form.cleaned_data.get('group'),
        )
        student.save()
        return super(AddStudentView, self).form_valid(form)

class AddGroupView(FormView):
    template_name = 'manage/manage_group.html'
    form_class = AddGroupForm
    success_url = '/'

    def form_invalid(self, form):
        return super(AddGroupView, self).form_invalid(form)

    def form_valid(self, form):
        group = Group.objects.create(
            name = form.cleaned_data.get('name'),
            main_student = form.cleaned_data.get('main_student'),
        )
        group.save()
        st = form.cleaned_data.get('main_student')
        student = Student.objects.get(pk=st.id)
        student.group = group
        student.save()
        return super(AddGroupView, self).form_valid(form)

class ManageStudentView(FormView):
    template_name = 'manage/manage_student.html'
    model = Student
    form_class = AddStudentForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ManageStudentView, self).get_context_data(**kwargs)
        context['student_detail'] = Student.objects.get(pk=self.kwargs['pk'])
        context['groups'] = Group.objects.all()
        return context

    def form_invalid(self, form):
        return super(ManageStudentView, self).form_invalid(form)

    def form_valid(self, form):
        student = Student.objects.get(pk=self.kwargs['pk'])
        student.fname = form.cleaned_data.get('fname')
        student.sname = form.cleaned_data.get('sname')
        student.lname = form.cleaned_data.get('lname')
        student.ticket = form.cleaned_data.get('ticket')
        student.group = form.cleaned_data.get('group')
        student.save()
        return super(ManageStudentView, self).form_valid(form)

class ManageGroupView(FormView):
    template_name = 'manage/manage_group.html'
    model = Group
    form_class = AddGroupForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ManageGroupView, self).get_context_data(**kwargs)
        context['group_detail'] = Group.objects.get(pk=self.kwargs['pk'])
        context['students'] = Student.objects.all()
        return context

    def form_invalid(self, form):
        return super(ManageGroupView, self).form_invalid(form)

    def form_valid(self, form):
        group = Group.objects.get(pk=self.kwargs['pk'])
        group.name = form.cleaned_data.get('name')
        group.main_student = form.cleaned_data.get('main_student')
        group.save()
        return super(ManageGroupView, self).form_valid(form)