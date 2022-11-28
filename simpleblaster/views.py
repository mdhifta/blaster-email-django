from django.shortcuts import render, redirect

#import models
from costumer.models import Form
from auth_log.models import Users

#alert import 
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def verify(request):
    if 'id_user' not in request.session:
        return redirect('login')

#function to dashboard
def dashboard(request):
    # check login verify
    verify(request)

    context = {}
    
    context['title'] = 'Blaster | Dashboard'
    context['account'] = request.session['nama_user']

    account = Form.objects.all()
    context['costumers'] = account

    return render(request, 'home/_dashboard.html', context)

def edit_pass(request):
    # check login verify
    verify(request)

    context = {}
    context['title'] = 'Blaster | Change Password'
    context['account'] = request.session['nama_user']
            
    return render(request, 'home/_password.html', context)

def edit_proses(request):
    # check login verify
    verify(request)
    
    id_user = request.session['id_user']

    if request.method == "POST":
        new_pass = request.POST['new_pass']
        con_pass = request.POST['con_pass']

        if new_pass == con_pass:
            new_password = make_password(new_pass)

            Users.objects.filter(id=id_user).update(password=new_password)

            messages.success(request, "Success update a password!")       
            return redirect('config-pass')
        else:
            messages.error(request, "Failed update a password. Confirm you password!")       
            return redirect('config-pass')

def logout(request):
    del request.session['id_user']
    del request.session['nama_user']

    return redirect('login')