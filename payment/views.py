from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action
import requests
from rest_framework.response import Response
import json
# Create your views here.
class PaymentViewSet(APIView):

    def get(self,request,*args,**kwargs):
        print(request.user)
        headers = {"X-Api-Key": "test_2accf58e3b53059e97169c873df", "X-Auth-Token": "test_4ab1f06cd9e3bcc0493e2ef4749"}
        payload = {
            'purpose': 'FIFA 16',
            'amount': '2500',
            'buyer_name': 'John Doe',
            'email': 'foo@example.com',
            'phone': '9999999999',
            'redirect_url': 'http://www.example.com/redirect/',
            'send_email': 'True',
            'send_sms': 'True',
            'webhook': 'http://www.example.com/webhook/',
            'allow_repeated_payments': 'False',
        }
        response = requests.post("https://test.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)
        return Response(json.loads(response.text))