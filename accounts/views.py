from django.shortcuts import render, redirect
from .forms import RegistrationForm, ResetPasswordForm
from .models import Account
from cart.models import Cart, CartItem
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages
from cart.utils import get_cart
from django.urls import reverse
import resend


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            # Store the cart before login
            old_cart = get_cart(request.session)
            old_cart_items = None
            if CartItem.objects.filter(cart=old_cart.cart).exists():
                old_cart_items = CartItem.objects.filter(cart=old_cart.cart)
            
            # Perform login - this creates a new session
            auth.login(request, user)
            
            # Get or create cart with new session
            new_cart = get_cart(request.session)
            
            # Transfer items from old cart to new cart if there were any
            if old_cart_items:
                for item in old_cart_items:
                    item.cart = new_cart.cart
                    item.user = user
                    item.save()
                
                # Delete the old cart
                old_cart.cart.delete()
            
            # Check for old items attached to the user
            old_user_items = CartItem.objects.filter(user=user, is_active=True)
            for item in old_user_items:
                item.cart = new_cart.cart
                item.save()


            # Create a response that triggers a cart update
            response = redirect('home')
            response['HX-Trigger'] = 'cartUpdate'
            return response
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('auth:login')
    
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

            params : resend.Emails.SendParams = {
                'from': "Acme <onboarding@resend.dev>",
                'to': [email],
                'subject': mail_subject,
                'html': message
            }

            resend.Emails.send(params)
            return redirect(f'{reverse("auth:login")}?command=verification&email={email}')

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
        messages.success(request, 'Your user has been activated')
        return redirect('home')
    else: 
        messages.error(request, 'Sorry we cannot activate your user')
        return redirect('home')
    

def password_recovery(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            mail_subject = 'Reset your bodyboost password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user': user,
                'domain': get_current_site(request),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })

            params : resend.Emails.SendParams = {
                'from': "Acme <onboarding@resend.dev>",
                'to': [email],
                'subject': mail_subject,
                'html': message
            }

            resend.Emails.send(params)
            messages.success(request, 'Password recovery email sent!')
            return redirect('auth:login')

        else:
            messages.error(request, 'Wrong email try again')
            return render(request, 'accounts/password_recovery.html')
        
    return render(request, 'accounts/password_recovery.html')


def reset_password_validation(request, uidb64, token):
    try: 
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        return redirect(reverse('auth:password_reset'))
    
    else:
        messages.error(request,'this link is not valid')
        return redirect('auth:login')


def password_reset(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        password = request.POST['password']
        
        if form.is_valid():
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset successful')
            return redirect('auth:login')
        
    else: 
        form = ResetPasswordForm()
    context = {'form': form}
    return render(request, 'accounts/reset_password.html', context)

