from home.models import student
import time
from django.core.mail import send_mail ,EmailMessage
from django.conf import settings

def run_this_function():
    print("Function Started ... ")
    print("Function Started ! ")

    time.sleep(1)
    print("Function Excecuted...")



def send_email_to_client():
    subject = "This email is from Django Server"
    message = "This is a test message from Django Server email"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["foramdelvadiya@gmail.com"]

    send_mail(subject , message ,from_email , recipient_list)


def send_email_with_attachment(subject , message , recipient_list , file_path):
    mail = EmailMessage(subject = subject , body = message , from_email = settings.EMAIL_HOST_USER , to = recipient_list )
   
    print(f"Attaching file: {file_path}")
    
    mail.attach_file(file_path)
    mail.send()