from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.forms import AccountForm, AccountUpdateForm
from account.models import Account
from account.utils import activation_send_html_email
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse_lazy


def register_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account until email confirmation
            user.save()
            current_site = get_current_site(request)
            
            if activation_send_html_email(user, current_site):
                messages.success(request, "Account created successfully!")
                return redirect("account:register_success") 
            else:
                messages.error(request, "Please Enter Correct Email Address")
        else:
            
            messages.error(request, f"Please correct the errors below.: {form.errors}")
    else:
        form = AccountForm()

    context = {
        "form": form,
        "page_title": "Account Registration"
    }
    return render(request, "account/register.html", context)
def register_success(request):
    return render(request, 'account/register-done.html')

User = get_user_model()
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('account:login')  # Redirect to login page after successful activation
    else:
        return render(request, 'registration/activation_failed.html')

def sign_in(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            print("Login successful!")
            return redirect("task:home")  # Replace "home" with the appropriate route name
        else:
            messages.error(request, "Invalid credentials.")
            print("Invalid credentials")
            return redirect("account:login")  # Replace "login" with the appropriate route name
    return render(request, "account/login.html")

@login_required
def sign_out(request):
    try:
        logout(request)
        messages.success(request, "Logged out successfully!")
        print("Logged out successfully!")
        return redirect("account:login")
    except Exception as e:
        print(f"Error logging out: {str(e)}")
        return redirect("account:login")  # Replace "login" with the appropriate route name
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/forget-password.html'
    email_template_name = 'utils/password_reset_email.html'
    success_url = reverse_lazy('account:password_reset_done')
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


@login_required
def profile_view(request):
    context = {
        'page_title': 'Profile',
        'user': request.user,
    }
    return render(request, 'account/profile.html', context)
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('account:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AccountForm(instance=request.user)
    context = {
        'page_title': 'Edit Profile',
        'form': form,
    }
    return render(request, 'account/profile-edit.html', context)

@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password change successfull')
            print("Password Change Successfully")
        else:
                        # Extracting the specific error message for 'old_password'
            old_password_error = form.errors.get('old_password', None)
            new_password2_error = form.errors.get('new_password2', None)
            if old_password_error:
                messages.error(request, old_password_error[0])  # Display the first error message only
            elif new_password2_error:
                messages.error(request, new_password2_error[0])  # Display the first error message only
            else:
                messages.error(request, f'Please correct the errors below.: {form.errors}')
                
                            # Extracting error messages for each field

    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'account/password_change.html', {'form': form})  