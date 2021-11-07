from django.db import models
from django.conf import settings


class Files(models.Model):
    name = models.TextField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name='Файл загрузил: ', blank=True, null=True)
    url = models.URLField(editable=None, max_length=200, verbose_name='Ссылка на файл', blank=True, null=True)
    poster = models.ImageField(verbose_name='Постер', upload_to='posters', blank=True, null=True)
    size = models.IntegerField(verbose_name='Размер файла', blank=True, null=True)

    def __str__(self):
        return str(self.name)