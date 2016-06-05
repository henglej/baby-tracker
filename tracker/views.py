from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    return render(request, 'login.html')

def userlogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'msg.html', {'success': False, 'message': 'Cannot login! Incorrect username or password.'})

def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
