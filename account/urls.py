from django.contrib.auth import views
from django.urls import path
from django.views.generic import TemplateView

from .forms import *
from .views import *

app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='account/registration/login.html', form_class=UserLoginForm), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('register/', account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>', account_activate, name='activate'),
    path('password_reset/', views.PasswordResetView.as_view(template_name='account/user/password_reset_form.html',
                                                            success_url='password_reset_email_confirm',
                                                            email_template_name='account/user/password_reset_email.html',
                                                            form_class=PwdResetForm), name='pwdreset'),
    
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/edit/', edit_details, name='edit_details'),
    path('profile/delete_user/', delete_user, name='delete_user'),
    path('profile/delete_cofirm/', TemplateView.as_view(template_name='account/user/delete_confirm.html'), name='delete_confirmation'),
]
