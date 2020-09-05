from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action
import requests
from rest_framework.response import Response
from rest_framework import viewsets
import json
from .models import *
from .serializers import *


# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=True)
    def hook(self, request, pk=None):
        print(request)
        return Response('')

    @action(detail=False)
    def get_link(self, request, pk=None):
        id = 'rzp_test_iMZWpZF2sYjm7v'
        sec = '9KI0fAguV70j37vrJhUfqZu6'
        print(request.user)
        import requests

        headers = {
            'Content-type': 'application/json',
        }
        t = '1'
        print(request.data)

        data = '{ "customer": { "name": "Acme Enterprises", "email": "admin@aenterprises.com", "contact": "9999999999" }, "type": "link", "view_less": 1, "amount": 670042, "currency": "INR", "description": "Payment Link for this purpose - cvb.", "receipt": ' + t + ', "reminder_enable": true, "sms_notify": 1, "email_notify": 1, "expire_by": 1793630556, "callback_url": "https://example-callback-url.com/", "callback_method": "get" }'

        response = requests.post('https://api.razorpay.com/v1/invoices/', headers=headers, data=data,
                                 auth=(id, sec))
        return Response(response.json())
