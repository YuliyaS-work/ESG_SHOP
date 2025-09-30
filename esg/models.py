from django.db import models
from django.forms import CharField


class Rubric(models.Model):
    '''
    Название основных разделов.
    Газовое оборудование, сантехника, электрика.
    '''
    rubric_name = models.CharField(max_length=50, verbose_name='Название раздела')

    class Meta:
        verbose_name_plural = 'Разделы'
        verbose_name = 'Раздел'
        ordering= ['rubric_name']

    def __str__(self):
        return self.rubric_name


class Electro(models.Model):
    '''Подразделы электрики.'''
    title = models.CharField(max_length=255, verbose_name='Подраздел электрики')
    rubric = models.ForeignKey(Rubric, on_delete = models.CASCADE, verbose_name='Раздел')

    class Meta:
        verbose_name_plural = 'Раздел "Электрика"'
        verbose_name = 'Раздел "Электрика"'
        ordering= ['title']

    def __str__(self):
        return self.title


class Gas(models.Model):
    '''Подразделы газового оборудования.'''
    title = models.CharField(max_length=255, verbose_name='Подраздел газового оборудования')
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, verbose_name='Раздел')

    class Meta:
        verbose_name_plural = 'Раздел "Газовое оборудование"'
        verbose_name = 'Раздел "Газовое оборудование"'
        ordering= ['title']

    def __str__(self):
        return self.title


class Santeh(models.Model):
    '''Подразделы сантехники.'''
    title = models.CharField(max_length=255, verbose_name='Подраздел сантехники')
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, verbose_name='Раздел')

    class Meta:
        verbose_name_plural = 'Раздел "Сантехника"'
        verbose_name = 'Раздел "Сантехника"'
        ordering= ['title']

    def __str__(self):
        return self.title

# Товары подразделов электрики
class ElectroProduct(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    photo = models.ImageField( upload_to='electro/', null=True, blank=True, verbose_name='Фото товара')
    code = models.PositiveIntegerField(null=True, blank=True, verbose_name='Код наименования')
    rubric = models.ForeignKey(Electro, on_delete = models.CASCADE, verbose_name='Электрика')

    class Meta:
        verbose_name_plural = 'Товары раздела электрики'
        verbose_name = 'Товар раздела электрики'
        ordering= ['title']



# Товары подразделов газового оборудования
class GasProduct(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    photo = models.ImageField(upload_to='gas/', null=True, blank=True, verbose_name='Фото товара')
    code = models.PositiveIntegerField(null=True, blank=True, verbose_name='Код наименования')
    rubric = models.ForeignKey(Gas, on_delete = models.CASCADE, verbose_name='Газовое оборудование')

    class Meta:
        verbose_name_plural = 'Товары раздела газового оборудования'
        verbose_name = 'Товар раздела газового оборудования'
        ordering= ['title']



# Товары подразделов сантехники
class SantehProduct(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    photo = models.ImageField(upload_to='santeh/', null=True, blank=True, verbose_name='Фото товара')
    code = models.PositiveIntegerField(null=True, blank=True, verbose_name='Код наименования')
    rubric = models.ForeignKey(Santeh, on_delete = models.CASCADE, verbose_name='Сантехника')

    class Meta:
        verbose_name_plural = 'Товары раздела сантехники'
        verbose_name = 'Товар раздела сантехники'
        ordering= ['title']