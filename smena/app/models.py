from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import valid_hour



class User(AbstractUser):
    name_of_company = models.CharField(max_length=250, blank=True, null=False, verbose_name='имя компании')


class Table(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='tables')
    name = models.CharField(max_length=250, blank=True, null=False, verbose_name='имя')
    date = models.DateField(verbose_name='дата')
    is_exists = models.BooleanField(default=False)


class Abstract(models.Model):
    fio = models.CharField(max_length=250, verbose_name='инициалы')
    cur_hours = models.IntegerField(default=0, validators=(valid_hour, ), verbose_name='отработано')
    graphic = models.CharField(max_length=32, verbose_name='график', default=' ')

    class Meta:
        abstract = True
        ordering = ('id', )

class Worker(Abstract):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workers', blank=True, null=True)
    


class AllWorkers(Abstract):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='allworkers', blank=True, null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='allworkers')

