from django.urls import path
from django.contrib.auth import views as auth_views
from account.views import (register_account, sign_in, activate, sign_out, register_success,
                           CustomPasswordResetCompleteView, CustomPasswordResetConfirmView,
                           CustomPasswordResetDoneView, CustomPasswordResetView, profile_view,
                           profile_edit, password_change )

app_name = 'account'

urlpatterns = [
    path("login/", sign_in, name="login"),
    path("register/", register_account, name="register"),
    path('register/success/', register_success, name='register_success'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path("logout/", sign_out, name="sign_out"),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('password_change/', password_change, name='password_change'),
]