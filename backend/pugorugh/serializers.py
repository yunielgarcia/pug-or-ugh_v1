from django.contrib.auth import get_user_model

from rest_framework import serializers
from . import models


class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserPref
        fields = ('age', 'gender', 'size')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        user_pref = models.UserPref.objects.create(
            user=user
        )
        user_pref.save()
        user.save()
        self.update_new_user_relation(user)
        return user

    def update_new_user_relation(self, user):
        dogs = models.Dog.objects.all()
        for dog in dogs:
            user_dog = models.UserDog.objects.create(
                user=user,
                dog=dog,
                status='u'
            )
            user_dog.save()

    class Meta:
        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dog
        fields = "__all__"


class UserDogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDog
        fields = "__all__"
