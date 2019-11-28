from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models.query import EmptyQuerySet
import numpy as np
import pandas_datareader as pr
import pandas as pd
import datetime
import xlrd
import sqlite3
from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# from django.core.exceptions import ObjectDoesNotExit
from django.http import Http404 
from .models import *
from django_pandas.io import read_frame
import csv,io
import reportlab
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from scipy import stats
import scipy
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import matplotlib.pyplot as plt
from pylab import *
from chartit import DataPool, Chart
import json
#import win32api
from jinja2 import Environment, FileSystemLoader
from json2html import *
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    
    return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
           'secret' : '6LcwbL4UAAAAABVgX4AgntMukd4hBdPJR6zIAb3A',
           'response' : recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if result['success']:
            user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
            user.save()
            messages.info(request,'Successful Registation!!')
            return redirect(request,'signup')
        else:
            messages.info(request,'Select The Valid Chepcha !!')
            return redirect(request,'signup')
    else:
        return render(request,'registration/signup.html')
    

def check_email(request):
    if request.method == "GET":
        raise Http404("URL doesn't exists")
    else:   
        response_data = {}
        login = request.POST["email"]
        user = None
        try:
            try:
                # we are matching the input again hardcoded value to avoid use of DB.
                # You can use DB and fetch value from table and proceed accordingly.
                if User.objects.filter(email=login).exists():
                    user = True
            except ObjectDoesNotExist as e:
                pass
            except Exception as e:
                raise e
            if not user:
                response_data["is_success"] = True
            else:
                response_data["is_success"] = False
        except Exception as e:
            response_data["is_success"] = False
            response_data["msg"] = "Some error occurred. Please let Admin know."

        return JsonResponse(response_data)

def check_login(request):
    if request.method == "GET":
        raise Http404("URL doesn't exists")
    else:   
        response_data = {}
        login = request.POST["uname"]
        user = None
        try:
            try:
                # we are matching the input again hardcoded value to avoid use of DB.
                # You can use DB and fetch value from table and proceed accordingly.
                if User.objects.filter(username=login).exists():
                    user = True
            except ObjectDoesNotExist as e:
                pass
            except Exception as e:
                raise e
            if not user:
                response_data["is_success"] = True
            else:
                response_data["is_success"] = False
        except Exception as e:
            response_data["is_success"] = False
            response_data["msg"] = "Some error occurred. Please let Admin know."

        return JsonResponse(response_data)

