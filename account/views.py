from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegistrationForm, UpdateUserForm, UpdateProfileForm


class RegisterView(CreateView):
    model = get_user_model()
    template_name = "account/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("account:register_done")


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(
            form.cleaned_data["password2"]
        )
        new_user.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, View):
    template_name = "registration/profile.html"

    
    def get(self, request, *args, **kwargs):
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        return render(request, self.template_name,
                      context={"user_form": user_form,
                               "profile_form": profile_form})


    def post(self, request, *args, **kwargs):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile is updated successfully")
            return redirect("account:profile")

        return render(request, self.template_name,
                      context={"user_form": user_form,
                               "profile_form": profile_form})
