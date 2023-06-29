from django.urls import path
from .views import (
    HelloView,
    MyLoginView, MyLogoutView, RegisterView, 
    ProfileUpdateView, ProfileDetailView, ProfileListView,
    FooBar,
    get_cookie_view, set_cookie_view,
    get_session_view, set_session_view,
    )


app_name = 'myauth'

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('', ProfileListView.as_view(), name='profiles'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('login/', MyLoginView.as_view(template_name='myauth/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change/<int:pk>/', ProfileUpdateView.as_view(), name='change'),

    path('cookie/get', get_cookie_view, name='get_cookie'),
    path('cookie/set', set_cookie_view, name='set_cookie'),
    path('session/get', get_session_view, name='get_session'),
    path('session/set', set_session_view, name='set_session'),
    path('session/foobar', FooBar.as_view(), name='foo-bar'),
]