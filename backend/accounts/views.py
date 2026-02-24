from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.http import JsonResponse
from .tokens import email_verification_token
import os 
from django.utils import timezone
from django.contrib.sessions.models import Session


User=get_user_model()

STREAMLIT_URL=os.getenv("STREAMLIT_BASE_URL")

def register_view(request):
    if request.method=="POST":
        email=request.POST["email"]
        password=request.POST["password"]

        if User.objects.filter(email=email).exists():
            return render(request,'register.html',{'error':'Email Exists'})
        
        user=User.objects.create_user(email=email,password=password)
        user.is_active=False
        user.save()
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        token=email_verification_token.make_token(user)

        link=request.build_absolute_uri(
            reverse('verify_email',kwargs={'uidb64':uid,'token':token})
        )

        send_mail("Verify Email",f"Click: {link}",settings.EMAIL_HOST_USER,[email])


        return render(request,"verify_email.html")
    return render(request,"register.html")

def verify_email(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except:
        user=None
    
    if user and email_verification_token.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect('login')
    return render(request,'verify_email.html')

def login_view(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']

        user=authenticate(request,email=email,password=password)

        if user:
            login(request,user)
            session_key=request.session.session_key
            return redirect(f"{STREAMLIT_URL}/?session={session_key}")
        else:
            return render(request,'login.html',{'error':'Invalid credentials'})
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def validate_session(request):
    session_key = request.GET.get("session")

    if not session_key:
        return JsonResponse({"valid": False})

    try:
        session = Session.objects.get(session_key=session_key)

        # Check if session is expired
        if session.expire_date > timezone.now():
            return JsonResponse({"valid": True})
        else:
            return JsonResponse({"valid": False})

    except Session.DoesNotExist:
        return JsonResponse({"valid": False})
