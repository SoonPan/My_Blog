from django.shortcuts import render

# Create your views here.
def life(request):
    return render(request, 'index/life.html')