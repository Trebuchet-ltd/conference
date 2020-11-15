import threading
from threading import Thread
from django.core.mail import send_mail
from django.conf import settings


class EmailThread(threading.Thread):
    def __init__(self, subject, content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.content = content
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.content, settings.EMAIL_HOST_USER, self.recipient_list, fail_silently=False)
        print(f'Mail [{self.subject}] sent to {self.recipient_list}')


def send_async_mail(subject, content, recipient_list):
    EmailThread(subject, content, recipient_list).start()
