from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        # Validasi sederhana
        if username and password and role:
            try:
                user = User.objects.create_user(username=username, password=password)
                UserProfile.objects.create(user=user, role=role)
                login(request, user)
                messages.success(request, "Registrasi berhasil, selamat datang!")
                return redirect('/module/')
            except Exception as e:
                messages.error(request, f"Error saat registrasi: {str(e)}")
        else:
            messages.error(request, "Semua field harus diisi!")
    return render(request, 'accounts/register.html')


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login berhasil!")
            return redirect('/module/')
        else:
            messages.error(request, "Username atau password salah.")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Anda telah logout.")
    return redirect('accounts:login')
