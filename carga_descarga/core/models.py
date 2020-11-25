from django.db import models

class Carga(models.Model):
    STATUS = (
        ('liberado', 'Liberado'),
        ('aguardando', 'Aguardando')
    )

    numero_nf = models.CharField('Numero NF', max_length=20)
    industria = models.CharField('Industria', max_length=20)
    dia_descarga  = models.DateField('Dia da descarga')
    status = models.CharField('Status', max_length=15, choices=STATUS)

    #Sempre que um registro for criado essa variável determina a data no BD
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.numero_nf
