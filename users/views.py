from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, CustomAuthenticationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string(
                'auth/email_confirmation.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                },
            )
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, 'auth/activation_sent.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'auth/activation_success.html')
    else:
        return render(request, 'auth/activation_failed.html')

def login_view(request):
    form = CustomAuthenticationForm(request)
    authentication_error = True
    
    if request.method == "POST":
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                authentication_error = False
                return redirect("customer:home")
    else:
        authentication_error = False
    
    auth_error_message = None
    if authentication_error:
        auth_error_message="Email or password was invalid"
    
    context = {
        "form": form,
        "authentication_error": auth_error_message
    }
    
    return render(request, "auth/login.html", context)

@login_required
def logout_view(request):
    logout(request)
    
    return redirect("frontend:home")
