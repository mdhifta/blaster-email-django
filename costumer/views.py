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


#function to add costumer
def add_costumer(request):
    verif = verify(request)
    
    if verif == False:
        return redirect('login')

    context = {}
    context['title'] = 'Blaster | Add Costumer'
    context['account'] = request.session['nama_user']

    if request.method == 'POST':
        name_costumer = request.POST['c_name']
        email = request.POST['email']
        whatsapp = request.POST['num_wa']
        description = request.POST['desc']
        jk = request.POST['jk']

        query = "INSERT INTO costumer_costumer(costumer_name, email_costumer, phone_costumer, gender_costumer, decription)  VALUES(%s, %s, %s, %s, %s)"
        val = (name_costumer, email, whatsapp, jk, description)
        cursor.execute(query, val)
        
        connect.commit()
        messages.success(request, "Success adding new costumer!")       
        
        return redirect('add-costumer')
        
    return render(request, 'costumers/add-costumer.html', context)

def list_costumer(request):
    verif = verify(request)
    
    if verif == False:
        return redirect('login')

    context = {}
    context['title'] = 'Blaster | List Costumer'
    context['account'] = request.session['nama_user']

    query = "SELECT * FROM costumer_costumer"
    cursor.execute(query)

    account = cursor.fetchall()

    #pagenation
    page = request.GET.get('page', 1)
    paginator = Paginator(account, 50)

    try:
        account = paginator.page(page)
    except PageNotAnInteger:
        account = paginator.page(1)
    except EmptyPage:
        account = paginator.page(paginator.num_pages)

    context['costumers'] = account

    return render(request, 'costumers/list-costumer.html', context)

def edit_show(request, id):
    verif = verify(request)
    
    if verif == False:
        return redirect('login')

    context = {}
    context['title'] = 'Blaster | Edit Costumer'
    context['account'] = request.session['nama_user']

    query = "SELECT * FROM costumer_costumer WHERE id = '{}'".format(id)
    cursor.execute(query)
        
    account = cursor.fetchall()

    for row in account:
        context['id_costumer'] = row['id']
        context['costumer_name'] = row['costumer_name']
        context['email_costumer'] = row['email_costumer']
        context['phone_costumer'] = row['phone_costumer']
        context['gender_costumer'] = row['gender_costumer']
        context['decription'] = row['decription']


    return render(request, 'costumers/edit-show.html', context)

def edit_proses(request):
    verif = verify(request)
    
    if verif == False:
        return redirect('login')

    if request.method == 'POST':
        id_costumer = request.POST['id']
        name_costumer = request.POST['c_name']
        email = request.POST['email']
        whatsapp = request.POST['num_wa']
        description = request.POST['desc']
        jk = request.POST['jk']

        query = "UPDATE costumer_costumer SET costumer_name = %s, email_costumer = %s, phone_costumer = %s, gender_costumer = %s, decription = %s WHERE id = %s"
        val = (name_costumer, email, whatsapp, jk, description, id_costumer)
        cursor.execute(query, val)
        
        #processing query
        connect.commit()

        messages.success(request, "Success updateing a costumer!")       
        return redirect('list-costumer')
    else:
        messages.error(request, "Failed updateing a costumer!")  
        return redirect('list-costumer')

def delete_proses(request, id):
    verif = verify(request)
    
    if verif == False:
        return redirect('login')
        
    id_costumer = id

    query = "DELETE FROM costumer_costumer WHERE id = {}".format(id_costumer)
    cursor.execute(query)
        
    #processing query
    connect.commit()

    messages.success(request, "Success deleted a costumer!")       
    return redirect('list-costumer')
        