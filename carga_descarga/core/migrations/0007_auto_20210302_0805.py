# Generated by Django 3.1.2 on 2021-03-02 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_auto_20210301_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carga',
            name='cor',
            field=models.CharField(max_length=8, verbose_name='cor'),
        ),
    ]