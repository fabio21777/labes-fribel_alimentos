from django.db import models
from django.contrib.auth.models import User

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
    tipo_entrada=models.CharField(max_length=40,blank=True)
    Produto=models.CharField(max_length=40,blank=True)
    QTD=models.CharField(max_length=40,blank=True)
    UN=models.CharField(max_length=40,blank=True)
    movimentacao=models.CharField(max_length=40,blank=True)
    frete=models.CharField(max_length=40,blank=True)
    observacao=models.CharField(max_length=200,blank=True)



    #Sempre que um registro for criado essa variável determina a data no BD
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.numero_nf
