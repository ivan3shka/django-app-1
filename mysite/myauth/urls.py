from venv import create

from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutPage,
    AboutMeView,
    RegisterView,
    FooBarView, UsersListView, UserDetailsView,

)

app_name  = 'myauth'

urlpatterns = [
    #path('login/', login_view, name='login'),
    path('login/',
         LoginView.as_view(
            template_name='myauth/login.html',
             redirect_authenticated_user=True,),
         name='login'),
    path('logout/', MyLogoutPage.as_view(), name='logout'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('users/', UsersListView.as_view(), name='users_list'),
    path('users/<int:pk>', UserDetailsView.as_view(), name='user_details'),
    path('register/', RegisterView.as_view(), name='register'),

    path('cookie/set/', set_cookie_view, name='set_cookie'),
    path('cookie/get/', get_cookie_view, name='get_cookie'),

    path('session/set/', set_session_view, name='set_session'),
    path('session/get/', get_session_view, name='get_session'),
    path('foo-bar/', FooBarView.as_view(), name='foo_bar'),
]