from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm)
from django.contrib.auth.views import (LoginView, PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import CreationForm, UserFormUpdate, ProfileFormUpdate


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class Login(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/login.html'


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'


class PasswordReset(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    template_name = 'users/password_reset_form.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy('users:password_reset_compete')
    template_name = 'users/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


# @login_required
# def update_profile(request, username):
#     user = get_object_or_404(User, username=username)
#     form_user = UserFormUpdate(request.POST or None,
#                                instance=user)
#     form_profile = ProfileFormUpdate(request.POST or None,
#                                      request.FILES or None,
#                                      instance=user.profile)
#     if form_user.is_valid() and form_profile.is_valid():
#         form_user.save()
#         form_profile.save()
#         return redirect('posts:profile', username)
#     context = {
#         'form_user': form_user,
#         'form_profile': form_profile
#     }
#     return render(request, '')

class UpdateUserData(FormView):
    form_class = UserFormUpdate
    template_name = 'users/user_profile.html'

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)