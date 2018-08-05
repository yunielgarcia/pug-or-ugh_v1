from . import views
from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.authtoken.views import obtain_auth_token

# API endpoints
urlpatterns = ([

    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),

    url(r'^api/user/$', views.UserRegisterView.as_view(), name='register-user'),

    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),

    url(r'^api/dog/(?P<pk>-?\d+)/(?P<opinion>liked|disliked|undecided)/next/$',
        views.RetrieveDog.as_view(),
        name='next'),

    url(r'^api/dog/(?P<dog_pk>-?\d+)/(?P<opinion_r>liked|disliked|undecided)/$',
        views.UserDogRelationUpdate.as_view(),
        name='relation'),

    url(r'^api/user/preferences/$', views.PreferenceRetrieveUpdate.as_view(), name='preferences-user'),

    url(r'^$', TemplateView.as_view(template_name='index.html'))
])
