# Generated by Django 3.0 on 2021-01-27 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_box_name1'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='box_reservado',
            field=models.CharField(blank=True, max_length=40, verbose_name='industria'),
        ),
        migrations.AddField(
            model_name='carga',
            name='dia_chegada',
            field=models.DateField(blank=True, default='2020-10-20', verbose_name='Dia da chegada'),
            preserve_default=False,
        ),
       
        
    ]