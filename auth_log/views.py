from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sessions.backends.base import UpdateError

#import models
from .models import Users
from mysql import connector
from operator import itemgetter

#alert import
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

#connection to mysql
from decouple import config

connect = connector.connect(host=config('DB_HOST'), user=config('DB_USERNAME'), passwd=config('DB_PASSWORD'), database=config('DB_NAME'))
cursor = connect.cursor(dictionary=True)

#function to login
def login(request):
    context = {}
    context['title'] = 'Blaster | Login'

    if request.method == "POST":
        #get post
        email = request.POST['email']
        password = request.POST['pass']

        query = "SELECT * FROM auth_log_users WHERE username = '{}'".format(email)
        cursor.execute(query)

        account = cursor.fetchall()

        #action to login
        if account == []:
            messages.error(request, "Email anda tidak dikenali!")
            return redirect('login')
        else:
            mypassword = ''
            for row in account:
                id_user = row['id']
                name_user = row['fname']+' '+row['lname']
                mypassword = row['password']

            if check_password(password, mypassword):
                request.session['id_user'] = id_user
                request.session['nama_user'] = name_user

                return redirect('dashboard')
            else:
                messages.error(request, "Password anda salah!")
                return redirect('login')

    return render(request, 'login_page.html', context)

#function to register
def register(request):
    context = {}
    context['title'] = 'Blaster | Register'

    if request.method == "POST":
        user = Users()

        #get post data
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.username = request.POST['username']
        user.password = make_password(request.POST['pass'])

        if user.fname == "" or user.password == "" or user.username == "":
            messages.info(request, "Tidak boleh kosong!")
            return redirect('register')
        else:
            messages.info(request, "Berhasil membuat akun!")
            user.save()
            return redirect('login')

    return render(request, 'register_page.html', context)
