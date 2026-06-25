from django.http import HttpResponse
from django.urls import path
from courses.views import hello_view

def home_view(request):
    return HttpResponse("Welcome to Course Management API")

urlpatterns = [
    path("", home_view),              # root path
    path("api/hello/", hello_view),   # hello endpoint
]
