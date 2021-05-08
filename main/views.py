# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import Http404
from mylogger import mylogger
# Create your views here

logger = mylogger('main-views').createLogger()

def index(request):
	return render(request,'main/index.html',{})
