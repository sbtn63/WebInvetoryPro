from django.shortcuts import render

def home_view(request):
    return render(request, "pages/core/home.html")
