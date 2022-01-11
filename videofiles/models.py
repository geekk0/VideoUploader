from django.db import models
from django.conf import settings


class Files(models.Model):
    name = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=200, verbose_name='Ссылка на файл', blank=True, null=True)
    size = models.IntegerField(verbose_name='Размер файла', blank=True, null=True)
    author = models.CharField(verbose_name='Имя (username)', max_length=60)
    contact_info = models.CharField(blank=True, null=True, verbose_name='Email', max_length=120)
    proxy_file = models.TextField(max_length=200, verbose_name='Файл для веб', blank=True, null=True)
    proxy_file_url = models.URLField(max_length=200, verbose_name='Ссылка на прокси файл',
                                     blank=True, null=True)
    author_desc = models.TextField(max_length=300, verbose_name="Описание ролика", blank=True, null=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return str(self.name)

    def get_proxy_name(self):
        self.proxy_file = self.name[:-3] + '.mp4'
