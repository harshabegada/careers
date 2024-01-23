from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from career_app.models import Careers_hub
from career_app.models import Career_feedback


def home(request):
    career_records=Careers_hub.objects.all()
    feedback_records=Career_feedback.objects.all()
    context={'feedback_records':feedback_records,'career_records':career_records}
    if request.method=="POST":
        f_name=request.POST.get('f_name')
        f_email=request.POST.get('f_email')
        f_rating=int(request.POST.get('f_rating'))
        feedback=request.POST.get('feedback')
        obj=Career_feedback(fullname=f_name,email=f_email,rating=f_rating,feedback=feedback)
        obj.save()
        messages.info(request,'Feedback inserted successfully')
        return render(request,'index.html',context)

    return render(request,'index.html',context)

def login_views(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are alredy Logged in...")
        if request.user.is_superuser:
            return redirect('AdminPanel')
        else:
            return redirect('User')
    if request.method=='POST':
        userName=request.POST.get('username')
        passWord=request.POST.get('password')
        user=authenticate(username=userName,password=passWord,is_activate=True)
        if user is not None:
            login(request,user)
            if request.user.is_superuser:
                messages.success(request,'Admin  you are successfully logged in..')
                return redirect('AdminPanel')
            else:
                messages.info(request,'normal user successfully login')
                return render(request,'user.html')
        else:
            messages.warning(request,'You enter wrong user or password')
            return render(request,'login.html')
    return render(request,'login.html')
    
@login_required(login_url='login')
def User_views(request):
    if request.method=='POST':  
        c_name=request.POST.get('c_name')
        c_link=request.POST.get('c_link')
        obj=Careers_hub(company_name=c_name,company_link=c_link)
        obj.save()
        messages.success(request,'You are inserted succecessfully..')
        return redirect('User')
    return render(request,'user.html') 

@login_required(login_url='login')
def admin_views(request):
    result=Career_feedback.objects.filter(status="pending")
    return render(request,'admin.html',{'data':result})

def feedback_approval(request,pk):
    if Career_feedback.objects.filter(id=pk).exists():
        obj=Career_feedback.objects.get(status='pending')
        obj.status='approved'
        obj.save()
        messages.info(request,'Feedback Approved...')
        return redirect('AdminPanel')
    else:
        messages.error(request,'Feedback Not Found...')
        return redirect('AdminPanel')
def feedback_delete(request,pk):
    if Career_feedback.objects.filter(id=pk).exists():
        obj=Career_feedback.objects.get(id=pk)
        obj.delete()
        messages.info(request,'You are successfully deleted pending feedbacks...')
        return redirect('AdminPanel')
    else:
        messages.warning(request,'You delete feedback not found')
        return redirect('AdminPanel')

def logout_views(request):
    logout(request)
    messages.info(request,'You are successfully logged out...')
    return redirect('login')


