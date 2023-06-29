from typing import Any
from random import random
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.urls import reverse, reverse_lazy
from django.views.generic import View, DetailView, CreateView, UpdateView, ListView
from django.utils.translation import gettext, gettext_lazy, ngettext
from .models import Profile
from .forms import ProfileForm


class HelloView(View):
    welcome_message = gettext_lazy('Welcome Hello World!')

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get('items') or 0
        items = int(items_str)
        products_line = ngettext(
            'one product',
            '{count} products',
            items
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f'<h1>{self.welcome_message}</h1>'
            f'<h2>{products_line}</h2>',
            )


class FooBar(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)
        return response

    def get_success_url(self) -> str:
        return reverse(
            'myauth:profile', kwargs={
                'pk': self.object.profile.pk
                },
        )


class ProfileListView(LoginRequiredMixin, ListView):
    queryset = Profile.objects.select_related('user')
    context_object_name = 'profiles'


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'myauth/update.html'

    def test_func(self) -> bool:
        return self.request.user.is_staff or self.request.user.profile.pk == self.kwargs['pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = ProfileForm(
            instance=self.object,
            initial={
                'first_name': self.object.user.first_name, 
                'last_name': self.object.user.last_name, 
                'email': self.object.user.email,
                }
        )
        return context

    def form_valid(self, form) -> HttpResponse:
        self.object.user.first_name = form.cleaned_data.get('first_name')
        self.object.user.last_name = form.cleaned_data.get('last_name')
        self.object.user.email = form.cleaned_data.get('email')
        self.object.user.save(
            update_fields=[
                'first_name','last_name', 'email',
                ]
            )
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse(
            'myauth:profile', kwargs={
                'pk': self.object.pk
                },
        )


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'myauth/profile_info.html'
    queryset = (
        Profile.objects.select_related('user')
    )


class MyLoginView(LoginView):
    def get_default_redirect_url(self):
        return reverse(
            'myauth:profile', kwargs={
                'pk': self.request.user.profile.pk
                },
        )


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response

@cache_page(timeout=100)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r} {random()}')


@permission_required('myauth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')



# def logout_view(request: HttpRequest) -> HttpResponse:
#     logout(request)
#     return redirect(reverse('myauth:login'))

# def login_view(request: HttpRequest) -> HttpResponse:
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             return redirect('/admin/')
        
#         return render(request, 'myauth/login.html')
    
#     username = request.POST['username']
#     password = request.POST['password']

#     user = authenticate(request, username=username, password=password)

#     if user:
#         login(request, user)
#         return redirect('/admin/')

#     return render(request, 'myauth/login.html', context={ 'error': 'Invalid login credentials' })