from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView)
from django.urls import path

from .views import (PasswordReset, PasswordResetComplete, PasswordResetConfirm,
                    PasswordResetDone, SignUp, UpdateUserData)

app_name = 'users'
urlpatterns = [
    path('logout/',
         LogoutView.as_view(
             template_name='users/logged_out.html'
         ),
         name='logout'
         ),
    path('signup/',
         SignUp.as_view(),
         name='signup'
         ),
    path('login/',
         LoginView.as_view(
             template_name='users/login.html'
         ),
         name='login'
         ),
    path('password_change/',
         PasswordChangeView.as_view(
             template_name='users/password_change.html'
         ),
         name='password_change'
         ),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'
         ),
         name='password_change_done'
         ),
    path('password_reset/',
         PasswordReset.as_view(
             template_name='users/password_reset_form.html'
         ),
         name='password_reset'
         ),
    path('password_reset/done/',
         PasswordResetDone.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'
         ),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirm.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'
         ),
    path('reset/done/',
         PasswordResetComplete.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_compete'
         ),
    path('update_profile/<username>/',
         UpdateUserData.as_view(),
         name='update_profile'
         )
]
