from django.shortcuts import render, redirect

# import models
from auth_log.models import Users

# alert import
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

# function to login
def login(request):
    context = {}
    context['title'] = 'Blaster | Login'

    if request.method == "POST":

        # get post
        email = request.POST['email']
        password = request.POST['pass']

        user = Users.objects.filter(username=email).first()

        # selection data none or not
        if user == None:
            messages.error(request, "Email anda tidak dikenali!")
            return redirect('login')
        else:
            if check_password(password, user.password):
                request.session['id_user'] = user.id
                request.session['nama_user'] = user.fname + ' ' + user.lname

                return redirect('dashboard')
            else:
                messages.error(request, "Password anda salah!")
                return redirect('login')

    return render(request, 'auth/_login.html', context)

# function to register
def register(request):
    context = {}
    context['title'] = 'Blaster | Register'

    if request.method == "POST":
        try:
            # check validation form
            if request.POST['fname'] == "" or request.POST['pass'] == "" or request.POST['username'] == "":
                messages.error(request, "Form Tidak boleh kosong!")
                return redirect('register')
            else:
                # check save data
                db = Users(fname=request.POST['fname'], lname=request.POST['lname'],
                           username=request.POST['username'], password=make_password(request.POST['pass']))
                db.save()
                messages.info(request, "Berhasil membuat akun!")
                return redirect('login')
        except:
            messages.error(request, "Email sudah digunakan")
            return redirect('register')

    return render(request, 'auth/_register.html', context)
