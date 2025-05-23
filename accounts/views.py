from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import json

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'store/login.html')
    
    return render(request, 'store/login.html')


def register(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username )
            user.save()
            
            # Email activation
            mail_subject = 'Activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': get_current_site(request),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('auth/login/?command=verification&email=' + email)

    else:        
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'store/register.html', context)

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    return redirect('home')


def activate(request,uidb64,token):
    try: 
        uuid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uuid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        #message here
        return redirect('home')
    else: 
        #message
        return redirect('home')
    

def password_recovery(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #Reset password 
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site, 
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            trigger = {
                   'showMessage': {
                    'message': 'Password recovery mail sent successfully',
                    'type': 'success',
                }
            }
            response['HX-Trigger'] = json.dumps(trigger)
            response = redirect('login')
            return response

        else:
            response = render(request, 'accounts/password_recovery.html')
            trigger = {
                'showMessage': {
                    'message': 'Wrong email',
                    'type': 'error',
                }
            }
            response['HX-Trigger'] = json.dumps(trigger)
            return response
        
    return render(request, 'accounts/password_recovery.html')


def reset_password_validation(request, uidb64, token):
    try: 
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        return redirect('password_reset')
    
    else:
        print('this link is not valid')
        return redirect('login')


def password_reset(request):
    if request.mehtod == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password()
            user.save()
            print('password reset successful')
            return redirect('login')
        else:
            print('password no not match')
            return redirect('password_reset')
    else: 
        return render(request, 'accounts/reset_password.html')

