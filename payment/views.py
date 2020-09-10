from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
import requests
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import views
import json
from .models import *
from .serializers import *
from rest_framework import status
from users.models import *
import datetime
import hmac
import hashlib

# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer


    def perform_create(self, serializer):
        print("here")

    @action(detail=True, methods=['post'])
    def hook(self, request, pk=None):
        data = request.data
        mac_provided = data.pop('mac')
        message = "|".join(v for k, v in sorted(data.items(), key=lambda x: x[0].lower()))
        # Pass the 'salt' without the <>.
        mac_calculated = hmac.new("94b0fe58a7ea44f6a09d38c53cb55531", message, hashlib.sha1).hexdigest()
        if mac_provided == mac_calculated:
            pay = Payments.objects.get(p_id=data['payment_id'])
            if data['status'] == "Credit":
                pay.status='done'
            # Payment was successful, mark it as completed in your database.
            else:
                pay.status='failed'
            pay.save()
            # Payment was unsuccessful, mark it as failed in your database.
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['post'])
    def get_link(self, request, pk=None):
        headers = {"X-Api-Key": "test_2accf58e3b53059e97169c873df", "X-Auth-Token": "test_4ab1f06cd9e3bcc0493e2ef4749"}
        val = User.objects.get(id=request.data["id"])

        if val.nationality=="India":
            payload = {
                'purpose': 'ISBIS Conference',
                'amount': 2500,
                'buyer_name': val.first_name,
                'email': val.email,
                'phone': val.phone,
                'redirect_url': 'http://www.example.com/redirect/',
                'send_email': 'True',
                'send_sms': 'True',
                'webhook': 'http://www.example.com/webhook/',
                'allow_repeated_payments': 'False',
            }
        else:
            rate = Rate.objects.first()
            date_1 = datetime.datetime.strptime(rate.updated_on, "%m/%d/%y")
            if date_1 == datetime.date.today():
                payload = {
                    'purpose': 'ISBIS Conference',
                    'amount': rate.rate*50,
                    'buyer_name': val.first_name,
                    'email': val.email,
                    'phone': val.phone,
                    'redirect_url': 'http://www.example.com/redirect/',
                    'send_email': 'True',
                    'send_sms': 'True',
                    'webhook': 'http://www.example.com/webhook/',
                    'allow_repeated_payments': 'False',
                }
            else:
                try:
                    r = requests.get('https://api.exchangeratesapi.io/latest?base=USD&symbols=INR')
                    print (r.json())
                    rate.rate=r.json()['rates']['INR']
                    rate.save()
                    payload = {
                        'purpose': 'ISBIS Conference',
                        'amount': rate.rate*50,
                        'buyer_name': val.first_name,
                        'email': val.email,
                        'phone': val.phone,
                        'redirect_url': 'http://www.example.com/redirect/',
                        'send_email': 'True',
                        'send_sms': 'True',
                        'webhook': 'http://www.example.com/webhook/',
                        'allow_repeated_payments': 'False',
                    }
                except :
                    payload = {
                        'purpose': 'ISBIS Conference',
                        'amount': rate.rate*50,
                        'buyer_name': val.first_name,
                        'email': val.email,
                        'phone': val.phone,
                        'redirect_url': 'http://www.example.com/redirect/',
                        'send_email': 'True',
                        'send_sms': 'True',
                        'webhook': 'http://www.example.com/webhook/',
                        'allow_repeated_payments': 'False',
                    }
        response = requests.post("https://test.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)
        s=json.loads(response.text)

        p = Payments()
        p.p_id=s["payment_request"]
        p.name=s['buyer_name']
        p.amount=s['amount']
        p.status=s['status']
        p.save()

        print (response.text)
        return Response(s["payment_request"]["longurl"])