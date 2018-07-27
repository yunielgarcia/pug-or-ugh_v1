from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from rest_framework.generics import CreateAPIView

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

        if req_opinion == 'undecided':
            matching_dogs = models.Dog.objects.exclude(
                users=user
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


class PreferenceRetrieveUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserPrefSerializer
    queryset = models.UserPref.objects.all()

    def retrieve(self, request, *args, **kwargs):
        preference = models.UserPref.objects.get(user=self.request.user)
        serializer = serializers.UserPrefSerializer(
            preference, many=False
        )
        return Response(serializer.data)

    def get_object(self):
        return get_object_or_404(
            self.get_queryset(),
            user=self.request.user
        )
