from django.contrib import admin
from main.models import Student, Group


class StudentInline(admin.TabularInline):
    model = Student
    extra = 1
    
class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fname', 'sname', 'lname', 'ticket', 'birthdate', 'group_name')
    list_filter = ('group', )
    search_fields = ('group', 'fname', 'sname', 'lname')

    def group_name(self, obj):
        return obj.group.name

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'sudent_fio')
    inlines = [StudentInline]

    def sudent_fio(self, obj):
        return '%s %s %s' % (obj.main_student.fname, obj.main_student.sname, obj.main_student.lname)

admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
