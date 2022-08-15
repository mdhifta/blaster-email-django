from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sessions.backends.base import UpdateError

#email setting
from django.conf import settings
from django.core.mail import send_mail

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

#function to sendmail
def sendmail(request):
    verif = verify(request)
    
    if verif == False:
        return redirect('login')

    context = {}
    context['title'] = 'Blaster | Send Email'
    context['account'] = request.session['nama_user']
    
    return render(request, 'send-mail.html', context)

def sendmail_process(request):
    verif = verify(request)
    
    if verif == False:
        return redirect('login')

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        email_from = settings.EMAIL_HOST_USER

        query = "SELECT * FROM costumer_costumer"
        cursor.execute(query)
        
        account = cursor.fetchall()

        #setting list email
        recipient_list = []

        for row in account:
             recipient_list.append(row['email_costumer'])

        send_mail(subject, message, email_from, recipient_list)

        messages.success(request, "Success send message to costumer!")     
        return redirect('send-email')