from django.shortcuts import render , redirect

# Create your views here.
from django.http import HttpResponse
from vege.seed import *
from .utils import send_email_to_client , send_email_with_attachment
from django.conf import settings
from home.models import Car

def send_email(request):
    subject = "This Email is from Django server with Attachment"
    message = "Hey please find this attach file with this email"
    recipient_list = ["foramdelvadiya@gmail.com"]

    file_path = f"{settings.BASE_DIR}/git-cheat-sheet-education.pdf"
    send_email_with_attachment(subject , message , recipient_list , file_path)

    return redirect('/')

def home(request):
    seed_db(100)

    Car.objects.create(car_name = f"Nexon-{random.randint( 0 , 100 )}")

    peoples = [
       {'name' : 'Abhijeet Gupta' , 'age' : 26 },
       {'name' : 'Deora Patel' , 'age' : 20 },
       {'name' : 'Deora Giri' , 'age' : 22 },
       {'name' : 'Hacker bhai' , 'age' : 16 },
       {'name' : 'LV Patel' , 'age' : 26 }
    ]

    for people in peoples:
        if people['age'] :
         print("Yes")

    vegetables = ['Potato', 'Tomato', 'Pumpkin']
    return render(request, "index.html", context = {'page':'Django 2024','peoples': peoples , 'vegetables': vegetables})
  

def about(request):
    context = {'page' : 'About'}
    return render(request , "about.html" )

def contact(request):
    context = {'page' : 'Contact'}
    return render(request , "contact.html" )

     
"""return HttpResponse("<h1>Hey ! i'm a DJango Server. </h1>
<br>
<p>Hey This is coming from Django server</p>
<br>
<h3>
Hope you are loving it :)</h3>")"""

"""Loren ipsum sit amet consectetur , adipisicing elit . Incidunt sequi consectetur quas , provident quo eligen
    In the Django Intro page, we learned that the result should be in HTML, and it should be created in a template, so let's do that.

Create a templates folder inside the members folder, and create a HTML file named myfirst.html...
"""

def success_page(request):
    print("*" * 10)
    context = {'page' : 'Contact'}
    return HttpResponse("<h1> Hey ! This is a Success Page ... </h1>")