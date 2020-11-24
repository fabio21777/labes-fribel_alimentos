from django.shortcuts import render

#def login(request):
 #   return render(request,'core\login.html')

def acomp(request):
    return render(request,'core/acomp.html')
def addCarga(request):
    return render(request,'core/adicionar_carga.html')
def login(request):
    return render(request,'core/login.html')
# Create your views here.
