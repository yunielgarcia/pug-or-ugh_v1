from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from django.http import Http404

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

        if req_opinion == 'undecided':
            queryset = preferred_dogs.filter(
                userdog__status='u',
                userdog__user_id=user.id
            ).order_by('pk')
        elif req_opinion == 'liked':
            queryset = preferred_dogs.filter(
                userdog__status='l',
                userdog__user_id=user.id
            ).order_by('pk')
        elif req_opinion == 'disliked':
            queryset = preferred_dogs.filter(
                userdog__status='d',
                userdog__user_id=user.id
            ).order_by('pk')

        user_pref = models.UserPref.objects.get(user=user)
        # mathing_dogs = models.Dog.objects.filter(
        #     gender__in=user_pref.gender.split(","),
        #     size__in=user_pref.size.split(","),
        #     # missing the age here
        # )
        mathing_dogs = models.Dog.objects.all()
        return mathing_dogs

    def get_object(self):
        """Getting dog from query_set ordered by pk"""
        pk = self.kwargs['pk']
        # GET first instance of Dog with a PK value > the URL

        current_dog = self.get_queryset().filter(id__gt=pk).first()
        return current_dog
