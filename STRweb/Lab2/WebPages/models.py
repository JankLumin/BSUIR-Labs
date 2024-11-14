from django.conf import settings
from django.db import models
from django.utils import timezone


class Banner(models.Model):
    image = models.ImageField(upload_to="banners/", verbose_name="Изображение баннера")
    link = models.URLField(verbose_name="Ссылка", blank=True, null=True)

    class Meta:
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

    def __str__(self):
        return f"Баннер {self.id}"


class Partner(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название компании")
    logo = models.ImageField(upload_to="partners_logos/", verbose_name="Логотип")
    website = models.URLField(verbose_name="Веб-сайт", blank=True, null=True)

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    rating = models.IntegerField(verbose_name="Оценка")
    comment = models.TextField(verbose_name="Комментарий")
    date_posted = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return (
            f"Отзыв от {self.user.username} на {self.date_posted.strftime('%Y-%m-%d')}"
        )


class PromoCode(models.Model):
    code = models.CharField(max_length=50, verbose_name="Код")
    active = models.BooleanField(default=True, verbose_name="Активен")
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Скидка (%)"
    )
    expiration_date = models.DateField(
        verbose_name="Дата окончания", blank=True, null=True
    )

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return f"{self.code} - {'активен' if self.active else 'неактивен'}"


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    summary = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полный текст")
    published_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )
    image = models.ImageField(
        upload_to="news/", verbose_name="Изображение", blank=True, null=True
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


class CompanyInfo(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название компании")
    logo = models.ImageField(
        upload_to="images/", verbose_name="Логотип", blank=True, null=True
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)

    about = models.TextField(
        verbose_name="Общая информация о компании", blank=True, null=True
    )

    history = models.TextField(verbose_name="История компании", blank=True, null=True)
    requisites = models.TextField(verbose_name="Реквизиты", blank=True, null=True)
    certificate_image = models.ImageField(
        upload_to="certificates/",
        verbose_name="Изображение сертификата",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=500, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    added_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Вопрос-ответ"
        verbose_name_plural = "Вопросы-ответы"

    def __str__(self):
        return self.question


class JobOpening(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название вакансии")
    description = models.TextField(verbose_name="Описание вакансии")
    location = models.CharField(
        max_length=200, verbose_name="Местоположение", blank=True
    )
    requirements = models.TextField(verbose_name="Требования", blank=True)
    responsibilities = models.TextField(verbose_name="Обязанности", blank=True)
    posted_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ["-posted_date"]

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Промокод",
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Корзина"
    )
    product_id = models.IntegerField(verbose_name="ID объекта недвижимости")
    product_type = models.CharField(
        max_length=50, verbose_name="Тип объекта недвижимости"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def __str__(self):
        return f"Товар {self.product_id} в корзине {self.cart.user.username}"
