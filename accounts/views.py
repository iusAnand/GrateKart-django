from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

#for register
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # fetching form data for creating user
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            #Creating user in Account model
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()

            # user activation by email verification
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            messages= render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                })
            to_email = email
            send_email = EmailMessage(mail_subject, messages, to=[to_email])
            send_email.send()

            messages.success(request, 'Registration successful.')
            return redirect('register')
    else:
        form = RegistrationForm()
    context={
        'form': form,
        }
    return render(request, 'accounts/register.html', context)

#for login
def login(request):
    #if user submits the login form
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        # if user have account user redirect to dashboard else back to login page
        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')


    return render(request, 'accounts/login.html')
    #if u are login then only u are able to logout
@login_required(login_url='login')
#for logout
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def activate(request):
    return