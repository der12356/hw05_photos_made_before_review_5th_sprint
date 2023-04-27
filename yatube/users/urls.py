from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView as PCDV
from django.contrib.auth.views import PasswordResetConfirmView as PRCV
from django.contrib.auth.views import PasswordResetCompleteView as PRV
from django.contrib.auth.views import (PasswordChangeView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.contrib.auth.views import LogoutView, LoginView

from . import views

app_name = 'users'

change_url = 'users/password_change_form.html'
done_url = 'users/password_reset_complete.html'
reset_done_url = 'users/password_reset_done.html'
reset_url = 'users/password_reset_form.html'

urlpatterns = [
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('password_change/done/',
         PCDV.as_view(template_name='users/password_change_done.html'),
         name='change_password_done'),
    path('password_change/',
         PasswordChangeView.as_view(template_name=change_url,
                                    success_url='change_password_done'),
         name='change_password'),
    path('reset/<uidb64>/<token>/',
         PRCV.as_view(template_name='users/password_reset_confirm.html',
                      success_url='reset/done/'), name='reset_confirm'),
    path('reset/done/', PRV.as_view(template_name=done_url),
         name='reset_complete'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name=reset_done_url),
         name='reset_done'),
    path('password_reset/',
         PasswordResetView.as_view(template_name=reset_url,
                                   success_url='done/'),
         name='reset_password')
]
