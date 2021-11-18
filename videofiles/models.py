from django.db import models
from django.conf import settings


class Files(models.Model):
    name = models.TextField(blank=True, null=True)
    url = models.URLField(editable=None, max_length=200, verbose_name='Ссылка на файл', blank=True, null=True)
    size = models.IntegerField(verbose_name='Размер файла', blank=True, null=True)

    def __str__(self):
        return str(self.name)