from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'profile'
router = DefaultRouter()
router.register(r'', views.FeedbackViewset)

urlpatterns = [
    # url('feedback', views.give_feedback, name='feedback'),
    url('participation_certificate/', views.get_participation_certificate, name='get_participation_certificate'),
    url('paper_certificate/', views.get_paper_certificate, name='get_paper_certificate'),
    url('session_certificate/', views.get_session_certificate, name='get_session_certificate'),
    url('reviewers', views.ReviewerList.as_view()),
    url('users', views.UserList.as_view()),
    url('registration/complete', views.complete_view, name='account_confirm_complete'),
    url('send_mail', views.SendMail.as_view()),
    url('anon_users', views.AnonPlenaryList.as_view()),
    url('delete_feedback/', views.delete_feedback, name='delete_feedback'),
    url('feedback/', include(router.urls))
]
