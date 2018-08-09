from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from . import models


# Create your tests here.

# MODELS

class DogModelTests(TestCase):

    def test_dog_creation(self):
        dog = models.Dog.objects.create(
            name='pluto',
            image_filename='2.jpg',
            breed='labrador',
            age=23,
            gender='m',
            size='l'
        )
        self.assertTrue(isinstance(dog, models.Dog))


class UserPreferenceModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='ygarcia',
            email='ygarcia@email.com'
        )

    def test_user_pref_creation(self):
        user_pref = models.UserPref.objects.create(
            user=self.user,
            age='b',
            gender='m',
            size='l'
        )
        self.assertTrue(isinstance(user_pref, models.UserPref))


class UserDogModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='ygarcia2',
            email='ygarcia2@email.com'
        )
        self.dog = models.Dog.objects.create(
            name='pluto',
            image_filename='22.jpg',
            breed='labrador',
            age=23,
            gender='m',
            size='l'
        )

    def test_user_dog_creation(self):
        user_dog = models.UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='l'
        )
        self.assertTrue(isinstance(user_dog, models.UserDog))


# Views
class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register-user')
        data = {'username': 'ygarcia', 'password': 'testpsw'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.User.objects.count(), 1)
        self.assertEqual(models.User.objects.get().username, 'ygarcia')
