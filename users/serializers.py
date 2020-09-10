from rest_framework import serializers
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_auth.registration.serializers import RegisterSerializer

from users.models import User, COUNTRY_OPTIONS, PAYMENT_STATUSES, GENDERS
from papers.serializers import PaperSerializer


class UserSerializer(serializers.ModelSerializer):
    # Just the titles.
    paper = serializers.StringRelatedField()

    # Populated
    # papers = PaperSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'paper']
        # fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'payment_status', 'nationality', 'paper',
        #           'role', 'profile_picture', 'address', 'designation', 'affiliation', 'gender', 'highest_degree',
        #           'subject', 'specialization']


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    phone = serializers.CharField(max_length=14)
    first_name = serializers.CharField(max_length=30, label='First Name')
    last_name = serializers.CharField(max_length=30, label='Last Name')
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    address = serializers.CharField(required=True, write_only=True)
    designation = serializers.CharField(required=True, write_only=True)
    affiliation = serializers.CharField(required=True, write_only=True)
    highest_degree = serializers.CharField(required=True, write_only=True)
    subject = serializers.CharField(required=True, write_only=True)
    specialization = serializers.CharField(required=True, write_only=True)
    gender = serializers.ChoiceField(choices=GENDERS)
    nationality = serializers.ChoiceField(choices=COUNTRY_OPTIONS)
    payment_status = serializers.ChoiceField(choices=PAYMENT_STATUSES)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.password = self.validated_data.get('passoword', '')
        user.phone = self.validated_data.get('phone', '')
        user.nationality = self.validated_data.get('nationality', '')
        user.payment_status = self.validated_data.get('payment_status', '')
        user.address = self.validated_data.get('address', '')
        user.designation = self.validated_data.get('designation', '')
        user.affiliation = self.validated_data.get('affiliation', '')
        user.highest_degree = self.validated_data.get('highest_degree', '')
        user.subject = self.validated_data.get('subject', '')
        user.specialization = self.validated_data.get('specialization', '')
        user.gender = self.validated_data.get('gender', '')
        user.save(update_fields=['first_name', 'last_name', 'payment_status', 'phone', 'nationality', 'address',
                                 'designation', 'affiliation', 'gender', 'highest_degree',
                                 'subject', 'specialization'])
