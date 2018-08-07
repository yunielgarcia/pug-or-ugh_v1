from django.contrib.auth.models import User
from django.db import models


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    size = models.CharField(max_length=2)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


# Profile model
class UserPref(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_pref')
    age = models.CharField(default='b', max_length=255)
    gender = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255, null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.user.username


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_dog')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='user_dog')
    status = models.CharField(max_length=1, default='u')

    def __str__(self):  # __unicode__ on Python 2
        return '{0} and {1}'.format(self.user.username, self.dog.name)


# Taking an average of 10 years of lifetime
# Taking for categories of age 'baby', 'young', 'adult', 'senior'
TIME_SPAN = int((10 * 12) / 4)
