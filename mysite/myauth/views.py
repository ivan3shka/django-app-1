from http.client import responses

from django.contrib.auth.decorators import (
                                            login_required,
                                            permission_required,
                                            user_passes_test,
                                            )


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView

from .forms import ProfileUpdateForm
from .models import Profile


# Create your views here.

@user_passes_test(lambda u: u.is_superuser) # проверяет, супер юзер ли юзер. Можно вписать и другие функ
def set_cookie_view(request:HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set ')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookie_view(request:HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r}')


@permission_required('myauth:view_profile', raise_exception=True) # сделает проверку, есть ли у user данное разрешение
def set_session_view(request:HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')


@login_required # сделает проверку, аутентифицирован ли пользователь
def get_session_view(request:HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default value')
    return HttpResponse(f'Session value: {value!r}')


class MyLogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('myauth:login')


class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = 'myauth/about-me.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get('username', self.request.user.username)
        user = get_object_or_404(User, username=username)

        context['profile_user'] = user
        context['form'] = ProfileUpdateForm(
            instance=user.profile) if user == self.request.user else None

        return context

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('myauth:about-me')
        return self.get(request, *args, **kwargs)

class UserDetailsView(DetailView):
    template_name = 'myauth/user_details.html'
    model = User
    context_object_name = 'user'

class RegisterView(CreateView):
    form_class = UserCreationForm # создаёт user
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form): # Вызывается когда форма была опубликована успешно. Здесь происходит сохранение объекта, а затем redirect
        response = super().form_valid(form)

        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get('username')
        password1 = form.cleaned_data.get('password1')
        user = authenticate(self.request,
                            username=username,
                            password=password1) # делаем аутентификацию пользователю
        login(request=self.request, user=user)
        return response # теперь при создании пользователя будет выполняться аутентификация


class UsersListView(ListView):
    model = User
    template_name = 'myauth/users_list.html'
    context_object_name = 'users'



class FooBarView(View):
    def get(self, request:HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})




