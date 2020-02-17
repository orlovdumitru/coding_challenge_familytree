from django.db import models
from django.core.serializers import serialize


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    created_by = models.CharField(max_length=70)
    updated_by = models.CharField(max_length=70)
    
    class Meta:
        abstract = True


class Person(TimeStamp):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    address = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        # return f"{first_name} {last_name}"
        return '{} {}'.format(first_name, last_name)


class RelationType(TimeStamp):
    type = models.CharField(max_length=20)


class Relation(TimeStamp):
    main_person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relation')
    relative = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relatives')
    relation = models.ForeignKey(RelationType, on_delete=models.CASCADE)
