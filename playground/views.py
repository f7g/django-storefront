from django.http.response import HttpResponse
from django.shortcuts import render


def say_hello(request):
    return render(request, 'hello.html', {'name': 'mario'})
