from PIL.ImageOps import deform
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Rubric(models.Model):
    '''
    Название основных разделов.
    Газификация, сантехника, электрика.
    '''
    rubric_name = models.CharField(max_length=50, verbose_name='Название раздела')

    class Meta:
        verbose_name_plural = 'Разделы'
        verbose_name = 'Раздел'
        ordering= ['-rubric_name']

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
    '''Подразделы газификации.'''
    title = models.CharField(max_length=255, verbose_name='Подраздел газификации')
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, verbose_name='Раздел')

    class Meta:
        verbose_name_plural = 'Раздел "Газификация"'
        verbose_name = 'Раздел "Газификация"'
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
    order = models.ManyToManyField('Order', verbose_name='Заказ', through='ElectroOrder')
    status_popular = models.BooleanField(default=False, verbose_name='Популярный товар')
    status_new = models.BooleanField(default=False, verbose_name='Новинка')
    counter = models.PositiveIntegerField(verbose_name='Количество заказов', default=0)

    class Meta:
        verbose_name_plural = 'Товары раздела "Электрика"'
        verbose_name = 'Товар раздела"Электрика"'
        ordering= ['title']



# Товары подразделов газификации
class GasProduct(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Цена')
    photo = models.ImageField(upload_to='gas/', null=True, blank=True, verbose_name='Фото товара')
    code = models.PositiveIntegerField(null=True, blank=True, verbose_name='Код наименования')
    rubric = models.ForeignKey(Gas, on_delete = models.CASCADE, verbose_name='Газификация')
    order = models.ManyToManyField('Order', verbose_name='Заказ', through='GasOrder')
    status_popular = models.BooleanField(default=False, verbose_name='Популярный товар')
    status_new = models.BooleanField(default=False, verbose_name='Новинка')
    counter = models.PositiveIntegerField(verbose_name='Количество заказов', default=0)

    class Meta:
        verbose_name_plural = 'Товары раздела "Газификация"'
        verbose_name = 'Товар раздела "Газификация"'
        ordering= ['title']



# Товары подразделов сантехники
class SantehProduct(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Описание товара')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    photo = models.ImageField(upload_to='santeh/', null=True, blank=True, verbose_name='Фото товара')
    code = models.PositiveIntegerField(null=True, blank=True, verbose_name='Код наименования')
    rubric = models.ForeignKey(Santeh, on_delete = models.CASCADE, verbose_name='Сантехника')
    order = models.ManyToManyField('Order', verbose_name='Заказ', through='SantehOrder')
    status_popular = models.BooleanField(default=False, verbose_name='Популярный товар')
    status_new = models.BooleanField(default=False, verbose_name='Новинка')
    counter = models.PositiveIntegerField(verbose_name='Количество заказов', default=0)

    class Meta:
        verbose_name_plural = 'Товары раздела "Сантехника"'
        verbose_name = 'Товар раздела "Сантехника"'
        ordering= ['title']



class Order(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя',  validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])
    last_name = models.CharField(max_length=255, verbose_name='Фамилия',  validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])
    phone = PhoneNumberField(region='BY', verbose_name='Телефон (+375 ХХ ХХХХХХХ)')
    mail = models.EmailField(verbose_name='Электронная почта', null=True, blank=True, default='')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    status = models.BooleanField(default=False, verbose_name='Статус заказа')
    general_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)
    agreement = models.BooleanField(verbose_name='Я даю согласие на обработку персональных данных')

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'
        ordering= ['date']

    def __str__(self):
        return f'{self.phone}, {self.date}'


class GasOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Номер заказа')
    gasproduct = models.ForeignKey(GasProduct, on_delete=models.CASCADE, verbose_name='Номер товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)

class ElectroOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Номер заказа')
    electroproduct = models.ForeignKey(ElectroProduct, on_delete=models.CASCADE, verbose_name='Номер товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)

class SantehOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Номер заказа')
    santehproduct = models.ForeignKey(SantehProduct, on_delete=models.CASCADE, verbose_name='Номер товара')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, default=0)


class Feedback(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя', validators =[RegexValidator(regex='^[A-Za-zА-Яа-яЁё]+$', message='Введите только буквы.', code='invalid_name')])
    phone = PhoneNumberField(region='BY', verbose_name='Телефон (+375 ХХ ХХХХХХХ)')
    subject = models.CharField(max_length=50, verbose_name='Тема', null=True, blank=True, default='')
    message = models.TextField(verbose_name='Ваше сообщение')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    status = models.BooleanField(default=False, verbose_name='Статус сообщения')
    agreement = models.BooleanField(verbose_name='Согласие на обработку персональных данных', default=False)

    class Meta:
        verbose_name_plural = 'Обратная связь'
        verbose_name = 'Обратная связь'
        ordering= ['date']

    def __str__(self):
        return f'{self.name}, {self.phone}, {self.date}'

