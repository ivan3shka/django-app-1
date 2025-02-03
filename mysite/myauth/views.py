from http.client import responses

from django.contrib.auth.decorators import (
                                            login_required,
                                            permission_required,
                                            user_passes_test,
                                            )


from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView
from .models import Profile


# Create your views here.

#def login_view(request:HttpRequest) -> HttpResponse:
#    if request.method == 'GET':
#        if request.user.is_authenticated:
#            return redirect('/admin/')
#
#        return render(request, 'muauth/login.html')
#
#    username = request.POST['username']
#    password = request.POST['password']
#
#    user = authenticate(request, username=username, password=password)
#
#    if user is not None:
#        login(request, user)
#        return redirect('/admin/')
#
#    return render(request, 'myauth/login.html',
#                 {'error': 'Invalid login credentials'})

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


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'


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
        return response # теперь при создании пользователя будет выполнятся аутентификация

class FooBarView(View):
    def get(self, request:HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})

