from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,StreamingHttpResponse
from django.http import Http404

# Create your views here.

def index(request):
	return render(request, 'index.html')
