from django.core.management import BaseCommand
from main.models import Group


class Command(BaseCommand):

    help = "Show groups and students"

    def handle(self, *args, **options):

        groups = Group.objects.all()

        for group in groups:
            print "#%s Group - %s (%s students)" % (group.id, group.name, len(group.student_set.all()))

            for student in group.student_set.all():
                print " -> #%s - %s %s %s : ticket #%s | birthdate %s" % (
                    student.id,
                    student.fname,
                    student.sname,
                    student.lname,
                    student.ticket,
                    student.birthdate
                )
