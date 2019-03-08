# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.settings import api_settings


@csrf_exempt
def check(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        username = params.get("username", "")
        if not User.objects.filter(username=str(username)).exists():
            return JsonResponse({"Message": "User not found", "Code": 1})
        else:
            return JsonResponse({"Message": "User found", "Code": 0})

    return HttpResponse(content="incorrect method", status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        params = json.loads(request.body)
        firstName = params.get("firstName", "")
        lastName = params.get("lastName", "")
        username = params.get("username", "")
        password = params.get("password", "")
        if not User.objects.filter(username=str(username)).exists():
            user = User.objects.create(
                username=username,
                email=str(username),
                first_name=firstName,
                last_name=lastName
            )
            user.set_password(password)
            user.save()
        else:
            user = User.objects.get(username=str(username))
            return JsonResponse({"Code": 1, "Message": "User Exist"})

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return JsonResponse({"Code": 0, "token": token, "user":{"id":user.id,"first_name":user.first_name, "last_name":user.last_name}})
        # now we are going to send a sms
    return HttpResponse(content="incorrect method", status=status.HTTP_404_NOT_FOUND)
