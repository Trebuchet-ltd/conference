from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'profile'

urlpatterns = [
    url('reviewers', views.ReviewerList.as_view()),
    url('users', views.UserList.as_view()),
    url('registration/complete', views.complete_view, name='account_confirm_complete'),
    url('send_mail', views.SendMail.as_view()),
    url('anon_users', views.AnonPlenaryList.as_view())
]
