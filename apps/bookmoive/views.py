from django.shortcuts import render

# Create your views here.
def bookmoive(request):
    return render(request, 'index/b&m.html')