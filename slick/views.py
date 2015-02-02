from django.contrib import messages
from django.views.generic import View, DetailView, FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model

from allauth.account.views import PasswordChangeView
from allauth.account.forms import ChangePasswordForm

from .forms import UserForm


class UserProfileDetailView(DetailView):
    model = get_user_model()
    template_name = "profile/detail.html"

    def get_object(self):
        return self.request.user


class UserProfileUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserForm
    template_name = "profile/update.html"
    view_name = 'profile-update'
    success_url = reverse_lazy(view_name)

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Profile updated')
        return super(UserProfileUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        context['change_password_form'] = ChangePasswordForm()
        return context
