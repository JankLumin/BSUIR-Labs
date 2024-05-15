from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings
import pytz
from tzlocal import get_localzone
import phonenumbers


class Article(models.Model):
    title = models.CharField(max_length=100)  # Заголовок статьи
    content = models.TextField()  # Содержание статьи
    publish_date = models.DateTimeField()  # Дата публикации
    image = models.ImageField(upload_to='media/', blank=True)  # Изображение статьи

    def __str__(self):
        return self.title

    def get_local_time(self):
        local_tz = get_localzone() # тут я получаю место (Europe/minks)
        local_time = self.publish_date.astimezone(local_tz)
        return local_time.strftime('%d-%m-%Y %H:%M:%S')

    def get_utc_time(self):
        local_time = self.publish_date.astimezone(pytz.utc)
        return local_time.strftime('%d-%m-%Y %H:%M:%S')


class Company(models.Model):
    info = models.TextField()  # Информация о компании


class News(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    image = models.ImageField(upload_to='media/', blank=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"  # Указывается правильное название в множественном числе


class FAQ(models.Model):
    question = models.CharField(max_length=100)  # Вопрос
    answer = models.TextField()  # Ответ
    added_date = models.DateField()  # Дата добавление


class Contact(models.Model):
    photo = models.ImageField(upload_to='media/', blank=True)  # Фото сотрудника
    description = models.TextField()  # Описание
    phone = models.CharField(max_length=20)  # Телефон
    email = models.EmailField()  # Почта

    def clean(self):
        # Проверка и форматирование номера телефона
        try:
            phone_number = phonenumbers.parse(self.phone, 'BY')  # 'BY' - код страны Беларусь
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError("Номер телефона не валиден")
            # Форматируем номер телефона к стандартному виду
            self.phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.NumberParseException:
            raise ValidationError("Номер телефона должен быть в формате +375 (29) XXX-XX-XX")


class Policy(models.Model):
    pass  # Пустое поле


class Vacancy(models.Model):
    title = models.CharField(max_length=100)  # Название вакансии
    description = models.TextField()  # Описание вакансии


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Имя автора отзыва
    rating = models.IntegerField()  # Оценка отзыва
    text = models.TextField()  # Текст отзыва
    date = models.DateField()  # Дата отзыва


class PromoCode(models.Model):
    code = models.CharField(max_length=50)  # Код промокода
    status = models.BooleanField()  # Статус промокода(активен или в архиве)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Manager'),
        ('manager', 'Client'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    birth_date = models.DateField(null=True)


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()


class Property(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey('PropertyType', on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='properties', on_delete=models.CASCADE)
    agents = models.ManyToManyField('Employee', related_name='properties')
    photo = models.ImageField(upload_to='property_images/', blank=True)
    num_rooms = models.IntegerField()
    area = models.DecimalField(max_digits=5, decimal_places=2)
    year_built = models.IntegerField()


class PropertyType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()


class Owner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()


class BuyerOrTenant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
