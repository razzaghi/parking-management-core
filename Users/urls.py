from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^check', views.check, name='check'),
    url(r'^register', views.register, name='register'),
    url(r'^login', obtain_jwt_token),
]
