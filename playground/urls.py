from playground.views import say_hello
from django.urls import path

urlpatterns = [
    path('say-hello/', say_hello)
]
