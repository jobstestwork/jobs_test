from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

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


TYPE_CREATED = 0
TYPE_MODIFIED = 1
TYPE_DELETED = 2

TYPES = (
    (TYPE_CREATED, 'Created'),
    (TYPE_MODIFIED, 'Modified'),
    (TYPE_DELETED, 'Deleted')
    )

class Log(models.Model):
    create_date = models.DateTimeField('Date', auto_now=True)
    type = models.CharField('Type', choices=TYPES, max_length=1)
    model = models.CharField('Class', max_length=200)
    log = models.CharField('Log', max_length=250)

    def __unicode__(self):
        return "%s: %s" % (self.create_date.strftime("%d.%m.%Y %H:%M"), self.log)

    class Meta:
        db_table = 'models_log'

@receiver(pre_save, sender=Student)
@receiver(pre_save, sender=Group)
def model_save_signal(sender, instance, signal, *args, **kwargs):
    h = Log()
    h.model = str(sender)
    try:
        sender.objects.get(pk=instance.pk)
        h.type = TYPE_MODIFIED
        h.log = 'modified'
    except sender.DoesNotExist:
        h.type = TYPE_CREATED
        h.log = 'created'
    h.log = 'Object <%s> ' % instance + h.log
    h.save()

@receiver(post_delete, sender=Student)
@receiver(post_delete, sender=Group)
def model_delete_signal(sender, instance, signal, *args, **kwargs):
    h = Log()
    h.model = str(sender)
    h.type = TYPE_DELETED
    h.log = 'Object <%s> was deleted' % instance
    h.save()