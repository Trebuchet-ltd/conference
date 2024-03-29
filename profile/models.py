from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

PAYMENT_STATUSES = [
    ('paid', 'paid'),
    ('not paid', 'not paid')
]

COUNTRIES = ["India", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina",
             "Armenia",
             "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
             "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei ",
             "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
             "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica",
             "Croatia", "Cuba", "Cyprus", "Czech Republic (Czechia)", "Côte d'Ivoire", "Denmark", "Djibouti",
             "Dominica", "Dominican Republic", "DR Congo", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
             "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia",
             "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
             "Holy See", "Honduras", "Hungary", "Iceland", "Indonesia", "Iran", "Iraq", "Ireland", "Israel",
             "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos",
             "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
             "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania",
             "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco",
             "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
             "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama",
             "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia",
             "Rwanda", "Saint Kitts & Nevis", "Saint Lucia", "Samoa", "San Marino", "Sao Tome & Principe",
             "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
             "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka",
             "St. Vincent & Grenadines", "State of Palestine", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria",
             "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
             "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
             "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]

COUNTRY_OPTIONS = [(country, country) for country in COUNTRIES]

ROLES = [
    ('speaker', 'speaker'),
    ('organiser', 'organiser'),
    ('viewer', 'viewer'),
    ('reviewer', 'reviewer'),
]

ANSWERS = [
    ('yes', 'Yes'),
    ('no', 'No'),
    ('maybe', 'Maybe'),
]

def media_location(instance, filename):
    return f'static/media/dp/{filename}'


def video_location(instance, filename):
    return f'static/media/sessions/{filename}'


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=500)
    payment_status = models.CharField(choices=PAYMENT_STATUSES, max_length=500, default='not paid')
    nationality = models.CharField(choices=COUNTRY_OPTIONS, max_length=500, default='India')
    profile_picture = models.FileField(upload_to=media_location, null=True, blank=True)
    designation = models.CharField(max_length=500, default='')
    affiliation = models.CharField(max_length=500, default='')
    highest_degree = models.CharField(max_length=500, default='')
    subject = models.CharField(max_length=500, default='')
    specialization = models.CharField(max_length=500, default='')
    redundant_role = models.IntegerField(default=0)
    recording = models.FileField(upload_to=video_location, null=True, blank=True)
    is_plenary = models.BooleanField(default=False)
    give_exception = models.BooleanField(default=False)
    feedback_submitted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    role = models.CharField(choices=ROLES, max_length=500, default='viewer')
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name.title()} {self.last_name.title()}, {self.affiliation}'


class Feedback(models.Model):
    user = models.OneToOneField(to=User, related_name='feedback', on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    affiliation = models.CharField(max_length=255)
    participation = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    session = models.CharField(max_length=255, null=True, blank=True)
    content = models.IntegerField(default=0, blank=True)
    satisfaction = models.IntegerField(default=0, blank=True)
    expectation = models.CharField(max_length=255, choices=ANSWERS, null=True, blank=True)
    interactive = models.CharField(max_length=255, choices=ANSWERS, null=True, blank=True)
    knowledge = models.CharField(max_length=255, choices=ANSWERS, null=True, blank=True)
    comments = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'
