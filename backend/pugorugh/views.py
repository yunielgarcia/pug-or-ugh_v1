from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from . import serializers
from . import models


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class RetrieveDog(generics.RetrieveAPIView):
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        """Getting all the dogs that match the user's preference"""
        user = self.request.user
        req_opinion = self.kwargs['opinion']
        matching_dogs = models.Dog.objects.all()
        span = models.TIME_SPAN

        size_pref = user.user_pref.size.split(',')
        gender_pref = user.user_pref.gender.split(',')
        # letters_for_age_ranges = user.user_pref.age.split(',')
        age_pref = user.user_pref.age.split(',')

        if req_opinion == 'undecided':
            matching_dogs = models.Dog.objects.filter(
                Q(age__in=list(range(1, span)) if 'b' in age_pref else [0]) |
                Q(age__in=list(range(span, span + 1)) if 'y' in age_pref else [0]) |
                Q(age__in=list(range(span * 2, span * 3 + 1)) if 'a' in age_pref else [0]) |
                Q(age__gte=90 if 's' in age_pref else 9999),  # 9999 impossible age for a dog
                gender__in=gender_pref,
                size__in=size_pref,
            ).exclude(
                Q(users=user) |
                Q(relation__status='u', relation__user=user.id)
            ).order_by('pk')
        elif req_opinion == 'disliked':
            matching_dogs = models.Dog.objects.filter(
                relation__status='d',
                relation__user=user.id
            ).order_by('pk')
        elif req_opinion == 'liked':
            matching_dogs = models.Dog.objects.filter(
                relation__status='l',
                relation__user=user.id
            ).order_by('pk')

        return matching_dogs

    def get_object(self):
        """Getting dog from query_set ordered by pk"""
        pk = self.kwargs['pk']

        current_dog = self.get_queryset().filter(id__gt=pk).first()
        if current_dog:
            return current_dog
        else:
            return self.get_queryset().first()

    @staticmethod
    def month_ranges(letters_for_age_ranges):
        print(letters_for_age_ranges)
        return letters_for_age_ranges


class PreferenceRetrieveUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserPrefSerializer
    queryset = models.UserPref.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            user=self.request.user
        )


class UserDogRelationUpdate(generics.UpdateAPIView):
    serializer_class = serializers.DogSerializer
    queryset = models.Dog.objects.all()

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            relation__user=self.request.user.pk,
            id=self.kwargs.get('dog_pk')
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # instance__relation__status=
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)