from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    size = models.CharField(max_length=2)
    users = models.ManyToManyField(User, through='UserDog', null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


# Profile model
class UserPref(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    size = models.CharField(max_length=255)

    def __str__(self):  # __unicode__ on Python 2
        return self.user.username


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relation')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='relation')
    status = models.CharField(max_length=1, default='u')

    def __str__(self):  # __unicode__ on Python 2
        return '{0} and {1}'.format(self.user.username, self.dog.name)
