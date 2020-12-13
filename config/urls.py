"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/auth/', include('rest_auth.urls')),
    path('api/auth/registration/', include('rest_auth.registration.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/papers/', include(('papers.urls', 'papers'), namespace='papers')),
    path('api/comments/', include(('comments.urls', 'comments'), namespace='comments')),
    path('api/profile/', include(('profile.urls', 'profile'), namespace='profile')),
    path('api/payment/', include('payment.urls')),
    path('api/talks/', include(('talks.urls', 'talks'), namespace='talks')),
    path('api/account/', include('allauth.urls')),
    path('api/notification/', include('notification.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/uploads/', include('uploads.urls')),
    path('api/stream/', include('stream.urls')),

]
#
# url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email,
#     name='account_confirm_email'),
