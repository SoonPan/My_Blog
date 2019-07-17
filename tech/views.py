from django.shortcuts import render

# Create your views here.
def tech(request):
    return render(request, 'index/tech.html')