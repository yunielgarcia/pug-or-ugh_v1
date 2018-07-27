from django.contrib.auth import get_user_model

from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = get_user_model()


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dog
        fields = "__all__"


class UserPrefSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = models.UserPref
        fields = ('age', 'gender', 'size')

    def get_age(self, obj):
        """Considering 10 years as average life time for dogs"""
        # total year in months / 4 to determine range of months
        # for each age ( "b" for baby, "y" for young, "a" for adult, "s" for senior)
        year_avg = 10
        num_clasif = 4
        period_changing_span = (year_avg * 12) / num_clasif
        span = int(period_changing_span)
        pref_age = int(obj.age)
        if pref_age in range(0, span + 1):
            return 'b'
        elif pref_age in range(span, (span * 2) + 1):
            return 'y'
        elif pref_age in range((span * 2), (span * 3) + 1):
            return 'a'
        else:
            return 's'

    # todo: Hacer conversion d letter a meses para la edad
