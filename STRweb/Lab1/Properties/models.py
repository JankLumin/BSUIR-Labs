from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


def property_directory_path(instance, filename):
    return f"property_{instance.content_object.id}/{filename}"


class Photo(models.Model):
    image = models.ImageField(
        upload_to=property_directory_path, verbose_name="Фотография"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"Фото для {self.content_object.title}"


class Property(models.Model):
    city = models.CharField(max_length=100, verbose_name="Населенный пункт или город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    building = models.CharField(max_length=20, verbose_name="Дом")
    building_section = models.CharField(
        max_length=20, verbose_name="Корпус", blank=True
    )
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    ownership = models.CharField(max_length=100, verbose_name="Форма собственности")
    transaction_condition = models.CharField(
        max_length=100, verbose_name="Условие сделки"
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    contacts = models.TextField(verbose_name="Контактные телефоны")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.city}, {self.street}, Дом {self.building}, Корпус {self.building_section if self.building_section else 'N/A'}"


class Apartment(Property):
    class Meta:
        verbose_name = "Квартиру"
        verbose_name_plural = "Квартиры"

    photos = GenericRelation(Photo)

    UNIT_TYPES = (
        ("apartment", "Квартира"),
        ("room", "Комната"),
        ("share_in_apartment", "Доля в квартире"),
    )
    unit_type = models.CharField(
        max_length=50, choices=UNIT_TYPES, verbose_name="Тип жилого объекта"
    )
    ROOM_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6+"),
    )
    rooms = models.IntegerField(choices=ROOM_CHOICES, verbose_name="Количество комнат")
    floor = models.IntegerField(verbose_name="Этаж")
    total_floors = models.IntegerField(verbose_name="Этажность")
    RENOVATION_CHOICES = (
        ("euro", "Евроремонт"),
        ("excellent", "Отличный"),
        ("good", "Хороший"),
        ("normal", "Нормальный"),
        ("satisfactory", "Удовлетворительный"),
        ("poor", "Плохое состояние"),
        ("emergency", "Аварийное состояние"),
        ("no_finish", "Без отделки"),
        ("construction_finish", "Строительная отделка"),
    )
    renovation = models.CharField(
        max_length=100, choices=RENOVATION_CHOICES, verbose_name="Ремонт", blank=True
    )
    BALCONY_CHOICES = (
        ("balcony", "Балкон"),
        ("none", "Нет"),
        ("loggia", "Лоджия"),
        ("balcony_and_loggia", "Балкон и лоджия"),
        ("terrace", "Терраса"),
    )
    balcony = models.CharField(
        max_length=50,
        choices=BALCONY_CHOICES,
        verbose_name="Балкон/лоджия",
        blank=True,
    )
    BATHROOM_CHOICES = (
        ("separate", "Раздельный"),
        ("combined", "Совмещенный"),
        ("two_or_more", "2 и более"),
    )
    bathroom = models.CharField(
        max_length=50, choices=BATHROOM_CHOICES, verbose_name="Санузел", blank=True
    )
    ceiling_height = models.FloatField(
        verbose_name="Высота потолков (м)", blank=True, null=True
    )
    total_area = models.FloatField(verbose_name="Общая площадь (кв. м)")
    living_area = models.FloatField(verbose_name="Жилая площадь (кв. м)")
    kitchen_area = models.FloatField(
        verbose_name="Площадь кухни (кв. м)", blank=True, null=True
    )
    year_built = models.IntegerField(
        verbose_name="Год постройки", blank=True, null=True
    )

    def __str__(self):
        return f"{self.rooms}-комн. квартира, {self.city}, {self.street}, Дом {self.building}, Этаж {self.floor}/{self.total_floors}"


class House(Property):
    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"

    photos = GenericRelation(Photo)

    HOUSE_TYPE_CHOICES = (
        ("house", "Дом"),
        ("cottage", "Коттедж"),
        ("summer_house", "Дача"),
        ("land_plot", "Участок"),
        ("half_house", "Полдома"),
        ("townhouse", "Таунхаус"),
    )
    house_type = models.CharField(
        max_length=20, choices=HOUSE_TYPE_CHOICES, verbose_name="Тип дома"
    )
    BEDROOM_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6+"),
    )
    bedrooms = models.IntegerField(
        choices=BEDROOM_CHOICES, verbose_name="Количество спален"
    )
    year_built = models.IntegerField(
        verbose_name="Год постройки", blank=True, null=True
    )
    WALL_MATERIAL_CHOICES = (
        ("brick", "Кирпичный"),
        ("panel", "Панельный"),
        ("block_room", "Блок-комнаты"),
        ("log", "Бревенчатый"),
        ("monolithic_frame", "Монолитно-каркасный"),
        ("silicate_blocks", "Силикатные блоки"),
    )
    wall_material = models.CharField(
        max_length=100,
        choices=WALL_MATERIAL_CHOICES,
        verbose_name="Материал стен",
        blank=True,
    )
    total_area = models.FloatField(verbose_name="Общая площадь (кв. м)")
    living_area = models.FloatField(verbose_name="Жилая площадь (кв. м)")
    kitchen_area = models.FloatField(
        verbose_name="Площадь кухни (кв. м)", blank=True, null=True
    )
    plot_area = models.FloatField(
        verbose_name="Площадь участка (сотки)", blank=True, null=True
    )
    WALL_MATERIAL_CHOICES = (
        ("elite_cottage", "Элитный коттедж"),
        ("euro_finish", "Евроотделка"),
        ("wood_finish", "Отделка деревом"),
        ("not_finished", "Не достроен"),
    )
    renovation = models.CharField(
        max_length=100,
        choices=WALL_MATERIAL_CHOICES,
        verbose_name="Ремонт",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Дом: {self.city}, {self.street}, Дом {self.building}, {self.bedrooms} спален, Участок {self.plot_area} соток"


class CommercialProperty(Property):
    class Meta:
        verbose_name = "Коммерскую невижимость"
        verbose_name_plural = "Коммерческая недвижимость"

    photos = GenericRelation(Photo)

    PROPERTY_TYPE_CHOICES = (
        ("office", "Офис"),
        ("retail_space", "Торговое помещение"),
        ("free_space", "Свободное помещение"),
        ("warehouse", "Склад"),
        ("manufacturing", "Производство"),
        ("food_service", "Общепит"),
        ("business", "Бизнес"),
        ("service_industry", "Сфера услуг"),
    )

    property_type = models.CharField(
        max_length=100, choices=PROPERTY_TYPE_CHOICES, verbose_name="Вид недвижимости"
    )
    separate_spaces_range = models.CharField(
        max_length=50,
        verbose_name="Количество раздельных помещений",
        blank=True,
        null=True,
    )
    floor = models.IntegerField(verbose_name="Этаж", blank=True, null=True)
    total_floors = models.IntegerField(
        verbose_name="Этажей в здании", blank=True, null=True
    )
    RENOVATION_CHOICES = (
        ("good", "Хороший"),
        ("normal", "Нормальный"),
        ("poor", "Плохое состояние"),
        ("no_finish", "Без отделки"),
        ("construction_finish", "Строительная отделка"),
    )
    renovation = models.CharField(
        max_length=100, choices=RENOVATION_CHOICES, verbose_name="Ремонт", blank=True
    )
    BATHROOM_CHOICES = (
        ("none", "Нет"),
        ("one", "Есть"),
        ("two", "2 санузла"),
    )
    bathroom = models.CharField(
        max_length=100, choices=BATHROOM_CHOICES, verbose_name="Санузел", blank=True
    )
    PHONE_LINE_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6+"),
    )
    phone_lines = models.IntegerField(
        verbose_name="Количество телефонов",
        choices=PHONE_LINE_CHOICES,
        blank=True,
        null=True,
    )
    ceiling_height = models.FloatField(
        verbose_name="Высота потолков", blank=True, null=True
    )
    WATER_SUPPLY_CHOICES = (
        ("none", "Нет"),
        ("yes", "Есть"),
        ("hot", "Горячая"),
        ("cold", "Холодная"),
    )
    water_supply = models.CharField(
        verbose_name="Водоснабжение",
        max_length=50,
        choices=WATER_SUPPLY_CHOICES,
        blank=True,
    )
    gas_supply = models.BooleanField(
        default=False, verbose_name="Газоснабжение", blank=True, null=True
    )
    ELECTRICITY_CHOICES = (
        ("no", "Нет"),
        ("yes", "Есть"),
        ("220v", "220В"),
        ("380v", "380В"),
    )
    electricity = models.CharField(
        verbose_name="Электричество",
        choices=ELECTRICITY_CHOICES,
        max_length=50,
        blank=True,
    )
    heating = models.BooleanField(
        default=False, verbose_name="Отопление", blank=True, null=True
    )
    WALL_MATERIAL_CHOICES = (
        ("block", "Блочный"),
        ("panel", "Панельный"),
        ("brick", "Кирпичный"),
        ("monolithic", "Монолитный"),
    )
    wall_material = models.CharField(
        max_length=100,
        choices=WALL_MATERIAL_CHOICES,
        verbose_name="Материал стен",
        blank=True,
    )
    space_area_range = models.CharField(max_length=50, verbose_name="Площадь помещений")
    plot_area = models.FloatField(verbose_name="Площадь участка", blank=True, null=True)
    BUILDING_CLASS_CHOICES = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
    )
    building_class = models.CharField(
        max_length=50,
        choices=BUILDING_CLASS_CHOICES,
        verbose_name="Класс здания",
        blank=True,
    )
    year_built = models.IntegerField(
        verbose_name="Год постройки", blank=True, null=True
    )
    has_legal_address = models.BooleanField(
        default=False, verbose_name="Наличие юридического адреса", blank=True
    )

    def __str__(self):
        return f"{self.property_type} на {self.floor} этаже, {self.city}, {self.street}, Дом {self.building}"


class Garage(Property):
    class Meta:
        verbose_name = "Гараж"
        verbose_name_plural = "Гаражи"

    photos = GenericRelation(Photo)

    GARAGE_TYPE_CHOICES = (
        ("garage", "Гараж"),
        ("parking_space", "Машиноместо"),
    )
    garage_type = models.CharField(
        max_length=100, choices=GARAGE_TYPE_CHOICES, verbose_name="Тип гаража"
    )
    separate_spaces = models.IntegerField(
        verbose_name="Количество раздельных помещений", blank=True, null=True
    )
    floor = models.IntegerField(verbose_name="Этаж", blank=True, null=True)
    total_floors = models.IntegerField(verbose_name="Этажность", blank=True, null=True)
    RENOVATION_CHOICES = (
        ("good", "Хороший"),
        ("normal", "Нормальный"),
        ("poor", "Плохое состояние"),
        ("no_finish", "Без отделки"),
        ("construction_finish", "Строительная отделка"),
    )
    renovation = models.CharField(
        max_length=100, choices=RENOVATION_CHOICES, verbose_name="Ремонт", blank=True
    )
    BATHROOM_CHOICES = (
        ("none", "Нет"),
        ("one", "Есть"),
        ("two", "2 санузла"),
    )
    bathroom = models.CharField(
        max_length=100, choices=BATHROOM_CHOICES, verbose_name="Санузел", blank=True
    )
    ceiling_height = models.FloatField(
        verbose_name="Высота потолков", blank=True, null=True
    )
    WATER_SUPPLY_CHOICES = (
        ("none", "Нет"),
        ("yes", "Есть"),
        ("hot", "Горячая"),
        ("cold", "Холодная"),
    )
    water_supply = models.CharField(
        choices=WATER_SUPPLY_CHOICES,
        verbose_name="Водоснабжение",
        blank=True,
        max_length=50,
    )
    gas_supply = models.BooleanField(
        default=False, verbose_name="Газоснабжение", blank=True, null=True
    )
    ELECTRICITY_CHOICES = (
        ("no", "Нет"),
        ("yes", "Есть"),
        ("220v", "220В"),
        ("380v", "380В"),
    )
    electricity = models.CharField(
        verbose_name="Электричество",
        choices=ELECTRICITY_CHOICES,
        blank=True,
        max_length=50,
    )
    heating = models.BooleanField(
        default=False, verbose_name="Отопление", blank=True, null=True
    )
    WALL_MATERIAL_CHOICES = (
        ("block", "Блочный"),
        ("panel", "Панельный"),
        ("brick", "Кирпичный"),
        ("monolithic", "Монолитный"),
    )
    wall_material = models.CharField(
        max_length=100,
        choices=WALL_MATERIAL_CHOICES,
        verbose_name="Материал стен",
        blank=True,
    )
    space_area = models.FloatField(verbose_name="Площадь помещений")
    year_built = models.IntegerField(
        verbose_name="Год постройки", blank=True, null=True
    )

    def __str__(self):
        return f"{self.garage_type}, {self.space_area} кв.м, {self.city}, {self.street}"


class ChangeRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "На рассмотрении"),
        ("approved", "Одобрено"),
        ("rejected", "Отклонено"),
    ]

    CHANGE_TYPE_CHOICES = [
        ("create", "Создание"),
        ("update", "Обновление"),
        ("delete", "Удаление"),
    ]

    property_type = models.CharField(max_length=50, verbose_name="Тип недвижимости")
    property_id = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="ID недвижимости"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    change_type = models.CharField(
        max_length=50, choices=CHANGE_TYPE_CHOICES, verbose_name="Тип изменения"
    )
    data = models.JSONField(verbose_name="Данные изменения", null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Запрос на изменение"
        verbose_name_plural = "Запросы на изменения"

    def __str__(self):
        return f"Запрос {self.id} от {self.user.username} - {self.change_type} {self.property_type}"
