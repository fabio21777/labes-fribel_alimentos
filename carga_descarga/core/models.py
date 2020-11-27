from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Box (models.Model):
    box_name = models.CharField('name',max_length=20)
          
    def __str__(self):        
        return self.box_name

class Carga(models.Model):
    STATUS = (
        ('liberado', 'Liberado'),
        ('aguardando', 'Aguardando')
    )

    numero_nf = models.CharField('Numero NF', max_length=40)
    industria = models.CharField('Industria', max_length=40)
    dia_descarga  = models.DateField('Dia da descarga')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField('Status', max_length=15, choices=STATUS)
    box = models.CharField('Box',default=' ',max_length=20,null=False)

    #Sempre que um registro for criado essa variável determina a data no BD
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.numero_nf
