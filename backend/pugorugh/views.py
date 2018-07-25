from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework import generics
from rest_framework import viewsets
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


class PreferenceViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserPrefSerializer

    def get_queryset(self):
        return models.UserPref.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        # call the original 'list'
        response = super(PreferenceViewSet, self).list(request, *args, **kwargs)
        # customize the response data
        response.data = response.data[0]
        return response  # return response with this custom representation