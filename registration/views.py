from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View


class RegisterView(View):
  def post(self, request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()          
      login(request, user)        
      return redirect('map:index')
    return render(request, 'registration/register.html', {'form': form})
  
  def get(self, request):
    form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class LoginView(View):
  def post(self, request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
          login(request, user)
          return redirect('map:index')
    return render(request, 'registration/login.html', {'form': form})
        
  def get(self, request):
    form = AuthenticationForm(data=request.POST or None)
    return render(request, 'registration/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('registration:login')