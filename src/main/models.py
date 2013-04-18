from django.db import models

class Student(models.Model):

    fname = models.CharField(max_length=255)
    sname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)

    image = models.ImageField(
        upload_to="students_images/%Y/%m/%d",
        blank=True,
        null=True
    )

    birthdate = models.DateField()
    ticket = models.CharField(max_length=255)
    group = models.ForeignKey('Group')

    def get_name(self):
        return "%s %s %s" % (self.fname, self.sname, self.lname)

    class Meta:
        db_table = 'students'

    def __unicode__(self):
        return "%s" % self.get_name()


class Group(models.Model):

    name = models.CharField(max_length=255)
    main_student = models.ForeignKey(Student, related_name='students')

    class Meta:
        db_table = 'groups'

    def __unicode__(self):
        return "%s" % self.name