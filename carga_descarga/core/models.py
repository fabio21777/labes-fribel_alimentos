from django.db import models
from django.contrib.auth.models import User


class Box(models.Model):
    name = models.CharField('Nome do Box', max_length=20)
    is_free = models.BooleanField('status do box', default=True)
    box_reservado = models.CharField('industria', max_length=40, blank=True)

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
    dia_chegada = models.DateField('Dia da chegada',blank=True)
    numero_nf = models.CharField('Numero NF', max_length=45)
    industria = models.CharField('Industria', max_length=40)
    dia_descarga = models.DateField('Dia da descarga',blank=True)
    user_ERP = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField('Status', max_length=15, choices=STATUS)
    tipo_entrada = models.CharField(max_length=20, blank=True)
    Produto = models.CharField(max_length=40, blank=True)
    QTD = models.CharField(max_length=10, blank=True)
    UN = models.CharField(max_length=12, blank=True)
    movimentacao = models.CharField(max_length=20, blank=True)
    frete = models.CharField(max_length=10, blank=True)
    observacao = models.CharField(max_length=500, blank=True)
    box = models.CharField('Box', max_length=20, blank=True)
    valor_carga = models.CharField(max_length=12, blank=True)
    numero_transacao = models.CharField(max_length=10, blank=True)
    # Sempre que um registro for criado essa variável determina a data no BD
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    cor = models.CharField('cor', max_length=10)
    is_ERP=models.BooleanField(default=False)
    checkin_carga=models.BooleanField(default=False)
    checkout_carga=models.BooleanField(default=False)

    

    def __str__(self):
        return (self.industria)
class Check(models.Model):
    CARGA = models.ForeignKey(Carga, on_delete = models.CASCADE)
    CHECKIN = models.BooleanField(default=False)
    CHECKIN_DATE = models.DateField('CHECKIN_DATE',blank=True)
    CHECKOUT = models.BooleanField(default=False)
    CHECKOUT_DATE = models.DateField('CHECKOUT_DATE',blank=True)

class Carga_Liberada(models.Model):
    STATUS = (
        ('liberado', 'Liberado'),
        ('aguardando', 'Aguardando')
    )

    numero_nf = models.CharField('Numero NF', max_length = 45)
    industria = models.CharField('Industria', max_length = 40)
    dia_descarga = models.DateField('Dia da descarga')
    user_ERP = models.CharField(max_length = 30, blank = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    status = models.CharField('Status', max_length = 15, choices = STATUS)
    tipo_entrada = models.CharField(max_length = 20, blank = True)
    Produto = models.CharField(max_length = 40, blank = True)
    QTD = models.CharField(max_length = 10, blank = True)
    UN = models.CharField(max_length = 12, blank = True)
    movimentacao = models.CharField(max_length = 20, blank = True)
    frete = models.CharField(max_length = 10, blank = True)
    observacao = models.CharField(max_length = 500, blank = True)
    box = models.CharField('Box', max_length = 20, blank = True)
    valor_carga = models.CharField(max_length = 12, blank = True)
    #Sempre que um registro for criado essa variável determina a data no BD
    created_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    finalizada = models.BooleanField(default = False)
    id = models.IntegerField(primary_key = True)

    def __str__(self):
        return self.numero_nf

class Itens_carga(models.Model):
    numero_pedido = models.CharField(max_length=10, blank=True)
    cod_prod = models.CharField(max_length=10, blank=True)
    descricao = models.CharField(max_length=100, blank=True)
    tipo_embalagem = models.CharField(max_length=2, blank=True)
    embalagem = models.CharField(max_length=20, blank=True)
    unidade = models.CharField(max_length=12, blank=True)
    departamento = models.CharField(max_length=30, blank=True)
    QTD_unitaria =  models.CharField(max_length=5, blank=True)
    QTD_caixa = models.CharField(max_length=5, blank=True)
    QTD_pedida = models.CharField(max_length=10, blank=True)
    QTD_reservada = models.CharField(max_length=10, blank=True)
    QTD_ult_entrada = models.CharField(max_length=10, blank=True)
    data_ultima_entrada = models.DateField('Dia da descarga')
    carga = models.ForeignKey(Carga, on_delete = models.CASCADE)
    numero_transacao = models.CharField(max_length=10, blank=True)