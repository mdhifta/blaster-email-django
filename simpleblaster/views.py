from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sessions.backends.base import UpdateError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#import models
from mysql import connector
from operator import itemgetter

#alert import 
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

#connection to mysql
from decouple import config

connect = connector.connect(host=config('DB_HOST'), user=config('DB_USERNAME'), passwd=config('DB_PASSWORD'), database=config('DB_NAME'))
cursor = connect.cursor(dictionary=True)

def verify(request):
    if 'id_user' not in request.session:
        return False

#function to dashboard
def dashboard(request):
    verif = verify(request)
    
    if verif == False:
        return redirect('login')

    context = {}
    context['title'] = 'Blaster | Dashboard'
    context['account'] = request.session['nama_user']

    query = "SELECT * FROM costumer_costumer ORDER BY id DESC LIMIT 8"
    cursor.execute(query)

    account = cursor.fetchall()

    context['costumers'] = account

    return render(request, 'dashboard_page.html', context)

def edit_pass(request):
    verif = verify(request)
    
    if verif == False:
        return redirect('login')

    context = {}
    context['title'] = 'Blaster | Change Password'
    context['account'] = request.session['nama_user']
            

    return render(request, 'change_password.html', context)

def edit_proses(request):
    verif = verify(request)
    
    if verif == False:
        return redirect('login')

    id_user = request.session['id_user']

    if request.method == "POST":
        new_pass = request.POST['new_pass']
        con_pass = request.POST['con_pass']

        if new_pass == con_pass:
            new_password = make_password(new_pass)

            query = "UPDATE auth_log_users SET password = %s WHERE id = %s"
            val = (new_password, id_user)
            cursor.execute(query, val)
        
            #processing query
            connect.commit()

            messages.success(request, "Success updateing a password!")       
            return redirect('config-pass')
        else:
            messages.error(request, "Failed updateing a password. Confirm you password!")       
            return redirect('config-pass')

def logout(request):
    del request.session['id_user']
    del request.session['nama_user']

    return redirect('login')