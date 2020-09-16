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
from profile.models import *
import datetime
import hmac
import hashlib
import codecs
from django.shortcuts import redirect


# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        print("here")

    @action(detail=True, methods=['get'])
    def redirect(self, request, pk=None):
        payment_id = request.query_params.get('payment_id')
        payment_request_id = request.query_params.get('payment_request_id')
        payment_status = request.query_params.get('payment_status')
        headers = {"X-Api-Key": "9433b167d61a543bf917d96c09a06150", "X-Auth-Token": "7176fd84bd8968e172c3f242fa8c1669"}

        response = requests.get(
            "https://www.instamojo.com/api/1.1/payments/" + str(payment_id) + "/",
            headers=headers)

        response_json = response.json()
        print(response_json)
        if (payment_status != None and payment_id != None and payment_request_id != None):
            try:
                pay = Payments.objects.get(p_id=payment_request_id)
                if (response_json["payment"]["status"] == payment_status):
                    if payment_status == "Credit":
                        pay.status = 'paid'
                        pay.location = 'URL'
                        PaymentUserSuccess = User.objects.get(id=pay.user_id)
                        PaymentUserSuccess.payment_status = 'paid'
                        PaymentUserSuccess.save()
                        pay.save()
            except:
                print('Error occured')
        return redirect('https://statconferencecusat.co.in/')

    @action(detail=True, methods=['post'])
    def hook(self, request, pk=None):
        data = request.data
        data = data.dict()
        print(data)
        mac_provided = data.pop('mac')
        message = "|".join(v for k, v in sorted(data.items(), key=lambda x: x[0].lower()))
        # Pass the 'salt' without the <>.
        mac_calculated = hmac.new(codecs.encode("c2e8b650e569459b9bc22b07b5ff8ff9"), codecs.encode(message),
                                  hashlib.sha1).hexdigest()
        if mac_provided == mac_calculated:
            pay = Payments.objects.get(p_id=data['payment_request_id'])
            if data['status'] == "Credit":
                pay.status = 'paid'
                pay.location = 'Webhook'
                PaymentUserSuccess = User.objects.get(id=pay.user_id)
                PaymentUserSuccess.payment_status = 'paid'
                PaymentUserSuccess.save()
            # Payment was successful, mark it as completed in your database.
            else:
                pay.status = 'failed'
            pay.save()
            # Payment was unsuccessful, mark it as failed in your database.
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def get_link(self, request, pk=None):
        headers = {"X-Api-Key": "9433b167d61a543bf917d96c09a06150", "X-Auth-Token": "7176fd84bd8968e172c3f242fa8c1669"}
        val = User.objects.get(id=request.data["id"])

        if val.nationality == "India":
            payload = {
                'purpose': 'ISBIS Conference',
                'amount': 1000,
                'buyer_name': val.first_name,
                'email': val.email,
                'phone': val.phone,
                'redirect_url': 'https://statconferencecusat.co.in/api/payment/redirect/redirect',
                'send_email': 'True',
                'send_sms': 'True',
                'webhook': 'https://statconferencecusat.co.in/api/payment/hook/hook/',
                'allow_repeated_payments': 'False',
            }
        else:
            rate = Rate.objects.first()
            date_1 = None
            if rate != None:
                date_1 = rate.updated_on
            if date_1 == datetime.date.today():
                payload = {
                    'purpose': 'ISBIS Conference',
                    'amount': round(rate.rate * 50, 2),
                    'buyer_name': val.first_name,
                    'email': val.email,
                    'phone': val.phone,
                    'redirect_url': 'https://statconferencecusat.co.in/api/payment/redirect/redirect',
                    'send_email': 'True',
                    'send_sms': 'True',
                    'webhook': 'https://statconferencecusat.co.in/api/payment/hook/hook/',
                    'allow_repeated_payments': 'False',
                }
            else:
                try:
                    r = requests.get('https://api.exchangeratesapi.io/latest?base=USD&symbols=INR')
                    rate.rate = r.json()['rates']['INR']
                    rate.save()
                    payload = {
                        'purpose': 'ISBIS Conference',
                        'amount': round(rate.rate * 50, 2),
                        'buyer_name': val.first_name,
                        'email': val.email,
                        'phone': val.phone,
                        'redirect_url': 'https://statconferencecusat.co.in/api/payment/redirect/redirect',
                        'send_email': 'True',
                        'send_sms': 'True',
                        'webhook': 'https://statconferencecusat.co.in/api/payment/hook/hook/',
                        'allow_repeated_payments': 'False',
                    }
                except:
                    payload = {
                        'purpose': 'ISBIS Conference',
                        'amount': round(rate.rate * 50, 2),
                        'buyer_name': val.first_name,
                        'email': val.email,
                        'phone': val.phone,
                        'redirect_url': 'https://statconferencecusat.co.in/api/payment/redirect/redirect',
                        'send_email': 'True',
                        'send_sms': 'True',
                        'webhook': 'https://statconferencecusat.co.in/api/payment/hook/hook/',
                        'allow_repeated_payments': 'False',
                    }
        response = requests.post("https://www.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)
        s = json.loads(response.text)

        print(s)
        p = Payments()
        p.p_id = s["payment_request"]['id']
        p.name = s["payment_request"]['buyer_name']
        p.amount = s["payment_request"]['amount']
        p.status = s["payment_request"]['status']
        p.user_id = request.data["id"]
        p.save()

        url = {"URL": s["payment_request"]["longurl"]}

        return Response(url, content_type="application/json; charset=UTF-8")
