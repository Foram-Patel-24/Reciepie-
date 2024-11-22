
from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.contrib.auth import get_user_model


User = get_user_model()


# Create your views here.

@login_required(login_url="/login/")
def receipes(request):
    if request.method == "POST":
     
        data = request.POST
 
        receipe_img = request.FILES.get('receipe_img')
        receipe_name = data.get('receipe_name')
        receipe_desc = data.get('receipe_desc')
     
        print(receipe_name)
        print(receipe_desc)  
        print(receipe_img)

        Receipe.objects.create(
            receipe_img = receipe_img,
            receipe_name = receipe_name,
            receipe_desc = receipe_desc,
        )

        return redirect('/receipes/')
    
    queryset = Receipe.objects.filter(is_deleted = False)

    if request.GET.get('search'):
       queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))


    context = {'receipes' : queryset}
         
    return render(request , 'receipes.html',context)

@login_required(login_url="/login/")
def update_receipe(request , slug):
    queryset = Receipe.objects.get(slug = slug)

    if request.method == "POST":

        data = request.POST

        receipe_img = request.FILES.get('receipe_img')
        receipe_name = data.get('receipe_name')
        receipe_desc = data.get('receipe_desc')

        queryset.receipe_name=receipe_name
        queryset.receipe_desc=receipe_desc

        if receipe_img:
            queryset.receipe_img=receipe_img


        queryset.save()
        return redirect('/receipes/')



    context = {'receipe' : queryset}
    return render(request , 'update_receipes.html',context)

@login_required(login_url="/login/")
def delete_receipe(request , id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipes/')


def login_page(request):

    if request.method == "POST":
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username = username , password = password)

        if user is None:
            messages.error(request , 'Invalid Password')
            return redirect('/login/')
        
        else:
            login(request , user)
            return redirect('/receipes/')
        


    return render(request , 'login.html')
        
def logout_page(request):
    logout(request)
    return redirect('/login/')


def register(request):

   if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():

            messages.error(request, 'Username already taken')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)
        user.save()

        messages.success(request, 'Account created successfully')

        return redirect('/register/')

        
        
        '''  else:
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully')

            login(request, user)
            return redirect('/receipes/') '''
        


   return render(request , 'register.html')     


from django.db.models import Q , Sum


def get_students(request):

    queryset = Student.objects.all()
       

    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            Q( student_name__icontains  = search ) |
            Q( department__department__icontains  = search ) |
            Q( student_id__student_id__icontains  = search ) |
            Q( student_email__icontains  = search ) |
            Q( student_age__icontains  = search )
        )

    paginator = Paginator(queryset , 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page" , 1)
    page_obj = paginator.get_page(page_number)

    print(page_obj.object_list)
    return render(request , 'report/students.html' , {'queryset' : page_obj})


from .seed import generate_report_card

def see_marks(request, student_id):
   
    queryset = SubjectMarks.objects.filter(student__student_id__student_id = student_id)
    total_marks = queryset.aggregate(total_marks=Sum('marks'))
    
    current_rank = -1

    ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks' , '-student_age')


    i=1

    for rank in ranks:

        print(rank.student_id)
        if student_id == rank.student_id.student_id:
            current_rank = i
            break
        i = i + 1
    
    
    return render(request, 'report/see_marks.html', {'queryset': queryset , 'total_marks': total_marks , 'current_rank' : current_rank})



