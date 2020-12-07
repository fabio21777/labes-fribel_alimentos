from django.db import models
from django.contrib.auth.models import User
class Box(models.Model):
    name = models.CharField('Nome do Box',max_length=20)
    is_free = models.BooleanField('status do box',default=True)
    def __str__(self):
        return self.name

class Tipo_user(models.Model):
    TIPO_USER = (
        ('Diretoria', 'diretoria'),
        ('CD', 'cd'),
        ('Padrao', 'padrao')
    )
    tipo_user = models.CharField('TIPO_USER', max_length = 15, choices = TIPO_USER)
    user_tipo = models.ForeignKey(User, on_delete = models.CASCADE, unique = True)
    
    def __str__(self):
        return self.tipo_user
class Carga(models.Model):
    STATUS = (
        ('liberado', 'Liberado'),
        ('aguardando', 'Aguardando')
    )

    numero_nf = models.CharField('Numero NF', max_length=45)
    industria = models.CharField('Industria', max_length=40)
    dia_descarga  = models.DateField('Dia da descarga')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField('Status', max_length=15, choices=STATUS)
    tipo_entrada=models.CharField(max_length=20,blank=True)
    Produto=models.CharField(max_length=40,blank=True)
    QTD=models.CharField(max_length=10,blank=True)
    UN=models.CharField(max_length=10,blank=True)
    movimentacao=models.CharField(max_length=20,blank=True)
    frete=models.CharField(max_length=10,blank=True)
    observacao=models.CharField(max_length=200,blank=True)
    box = models.CharField('Box',max_length=20,blank=True)
    #Sempre que um registro for criado essa variável determina a data no BD
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    finalizada=models.BooleanField(default=False)

    def __str__(self):
        return self.numero_nf
