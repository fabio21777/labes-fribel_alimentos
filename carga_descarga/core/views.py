from django.shortcuts import render

def acomp(request, usuario):
    return render(request,'core/acomp.html', {'usuario': usuario})
def addCarga(request):
    return render(request,'core/adicionar_carga.html')
def login(request):
    return render(request,'core/login.html')
