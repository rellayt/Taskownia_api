import uuid

from django.db import models


# Create models
class User(models.Model):
    class Meta:
        db_table = 'user'

    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    personal_data = models.ForeignKey('PersonalData', on_delete=models.CASCADE, null=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __getitem__(self, key):
        return getattr(self, key)


class PersonalData(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=12)
    birth_date = models.DateField(null=True, blank=True)

    def __getitem__(self, key):
        return getattr(self, key)


class Address(models.Model):
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=60)
    country = models.CharField(max_length=60)
    zip_code = models.IntegerField(null=True, blank=True)

    def __getitem__(self, key):
        return getattr(self, key)

# class Project(models.Model):
#     author = models.ForeignKey('User', on_delete=models.DO_NOTHING())
#     title = models.CharField(max_length=50)
##      date
