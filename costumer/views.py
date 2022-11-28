from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#import models
from costumer.models import Form

# alert import
from django.contrib import messages

def verify(request):
    if 'id_user' not in request.session:
        return redirect('login')


# function to add costumer
def add_costumer(request):
    # verify to login
    verify(request)

    context = {}
    context['title'] = 'Blaster | Add Costumer'
    context['account'] = request.session['nama_user']

    if request.method == 'POST':
        # check save data
        db = Form(costumer_name=request.POST['c_name'], email_costumer=request.POST['email'],
                  phone_costumer=request.POST['num_wa'], gender_costumer=request.POST['jk'],
                  decription=request.POST['desc'])
        db.save()

        messages.success(request, "Success adding new costumer!")
        return redirect('add-costumer')

    return render(request, 'costumers/_add.html', context)


def list_costumer(request):
    # check verify login
    verify(request)

    context = {}
    context['title'] = 'Blaster | List Costumer'
    context['account'] = request.session['nama_user']

    account = Form.objects.all()

    # pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(account, 50)

    try:
        account = paginator.page(page)
    except PageNotAnInteger:
        account = paginator.page(1)
    except EmptyPage:
        account = paginator.page(paginator.num_pages)

    context['costumers'] = account

    return render(request, 'costumers/_list.html', context)


def edit_show(request, id):
    # check verify login
    verify(request)

    context = {}
    context['title'] = 'Blaster | Edit Costumer'
    context['account'] = request.session['nama_user']

    user = Form.objects.filter(id=id).first()

    context['id_costumer'] = user.id
    context['costumer_name'] = user.costumer_name
    context['email_costumer'] = user.email_costumer
    context['phone_costumer'] = user.phone_costumer
    context['gender_costumer'] = user.gender_costumer
    context['decription'] = user.decription

    return render(request, 'costumers/_edit.html', context)

def edit_proses(request):
    # verify login
    verify(request)

    if request.method == 'POST':
        Form.objects.filter(id=request.POST['id']).update(costumer_name=request.POST['c_name'], email_costumer=request.POST['email'],
        phone_costumer=request.POST['num_wa'], gender_costumer=request.POST['jk'], decription=request.POST['desc'])

        messages.success(request, "Success updateing a costumer!")
        return redirect('list-costumer')
    else:
        messages.error(request, "Failed updateing a costumer!")
        return redirect('list-costumer')


def delete_proses(request, id):
    # check login verify
    verify(request)

    Form.objects.filter(id=id).delete()
    messages.success(request, "Success deleted a costumer!")

    return redirect('list-costumer')
