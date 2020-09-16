from rest_framework import serializers
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_auth.registration.serializers import RegisterSerializer

from profile.models import User, COUNTRY_OPTIONS, PAYMENT_STATUSES
from papers.serializers import PaperSerializer
from talks.serializers import SessionSerializer


class UserSerializer(serializers.ModelSerializer):
    # Just the titles.
    paper = serializers.StringRelatedField()
    poster = serializers.StringRelatedField()
    session_organising = SessionSerializer()

    # Populated
    # papers = PaperSerializer(many=True)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups',
                   'user_permissions']
        extra_kwargs = {
            'payment_status': {'read_only': True},
            'role': {'read_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['session_organising']:
            data['session_organising'] = ''
        return data


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    phone = serializers.CharField(max_length=14)
    first_name = serializers.CharField(max_length=30, label='First Name')
    last_name = serializers.CharField(max_length=30, label='Last Name')
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    designation = serializers.CharField(required=True, write_only=True)
    affiliation = serializers.CharField(required=True, write_only=True)
    highest_degree = serializers.CharField(required=True, write_only=True)
    subject = serializers.CharField(required=True, write_only=True)
    specialization = serializers.CharField(required=True, write_only=True)
    nationality = serializers.ChoiceField(choices=COUNTRY_OPTIONS)
    # payment_status = serializers.ChoiceField(choices=PAYMENT_STATUSES)
    redundant_role = serializers.IntegerField()

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.password = self.validated_data.get('passoword', '')
        user.phone = self.validated_data.get('phone', '')
        user.nationality = self.validated_data.get('nationality', '')
        # user.payment_status = self.validated_data.get('payment_status', '')
        user.designation = self.validated_data.get('designation', '')
        user.affiliation = self.validated_data.get('affiliation', '')
        user.highest_degree = self.validated_data.get('highest_degree', '')
        user.subject = self.validated_data.get('subject', '')
        user.specialization = self.validated_data.get('specialization', '')
        user.save(update_fields=['first_name', 'last_name', 'payment_status', 'phone', 'nationality',
                                 'designation', 'affiliation', 'highest_degree',
                                 'subject', 'specialization'])
