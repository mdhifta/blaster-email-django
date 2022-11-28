from django.shortcuts import render, redirect

#email setting
from django.conf import settings
from django.core.mail import send_mail

#import models
from costumer.models import Form

#alert import 
from django.contrib import messages

def verify(request):
    if 'id_user' not in request.session:
        return redirect('login')

#function to sendmail
def sendmail(request):
    # verify login 
    verify(request)

    context = {}
    context['title'] = 'Blaster | Send Email'
    context['account'] = request.session['nama_user']
    
    return render(request, 'mail/_send_mail.html', context)

def sendmail_process(request):
    # verify login
    verify(request)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        email_from = settings.EMAIL_HOST_USER
        
        account = Form.objects.all()

        #setting list email
        recipient_list = []

        for row in account:
             recipient_list.append(row.email_costumer)

        send_mail(subject, message, email_from, recipient_list)

        messages.success(request, "Success send message to costumer!")     
        return redirect('send-email')