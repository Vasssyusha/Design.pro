import uuid
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class DesignStyle(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название стиля")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Стиль оформления"
        verbose_name_plural = "Стили оформления"

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название материала")

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    def __str__(self):
        return self.name


class Room(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('done', 'Готово'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name='rooms')
    title = models.CharField(max_length=200, verbose_name="Название помещения")
    room_type = models.CharField(
        max_length=50,
        choices=[
            ('living', 'Гостиная'),
            ('bedroom', 'Спальня'),
            ('kitchen', 'Кухня'),
            ('bathroom', 'Ванная'),
            ('office', 'Кабинет'),
            ('other', 'Другое'),
        ],
        verbose_name="Тип помещения"
    )
    area = models.FloatField(verbose_name="Площадь (м²)", null=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Описание пожеланий", help_text="Опишите, как вы хотите оформить это помещение")
    plan_image = models.ImageField(upload_to='room_plans/', verbose_name="План помещения", help_text="Загрузите план или фото помещения")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"
        permissions = (("can_make_proposal", "Предлагать варианты оформления"),)

    def __str__(self):
        return f"{self.title} ({self.get_room_type_display()})"

    def get_absolute_url(self):
        return reverse('room-detail', args=[str(self.id)])


class DesignProposal(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    style = models.ForeignKey(DesignStyle, on_delete=models.SET_NULL, null=True, verbose_name="Стиль")
    materials = models.ManyToManyField(Material, blank=True, verbose_name="Материалы")
    preview_image = models.ImageField(upload_to='proposals/', blank=True, verbose_name="Изображение")
    room_type = models.CharField(
        max_length=20,
        choices=[
            ('bedroom', 'Спальня'),
            ('bathroom', 'Ванная'),
            ('kitchen', 'Кухня'),
            ('living_room', 'Гостиная'),
            ('office', 'Офис'),
            ('other', 'Другое'),
        ],
        default='other',
        verbose_name="Тип помещения"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Вариант оформления"
        verbose_name_plural = "Варианты оформления"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('proposal-detail', args=[str(self.id)])


class Designer(models.Model):
    first_name = models.CharField(max_length=100, default='', verbose_name="Имя")
    last_name = models.CharField(max_length=100, default='', verbose_name="Фамилия")
    experience_years = models.IntegerField(default=0, verbose_name="Стаж работы (лет)")
    phone = models.CharField(max_length=20, default='', verbose_name="Номер телефона")
    photo = models.ImageField(upload_to='designers/', blank=True, verbose_name="Фото")
    bio = models.TextField(blank=True, verbose_name="Биография")

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Дизайнер"
        verbose_name_plural = "Дизайнеры"

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse('designer-detail', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        ordering = ['name']
        verbose_name = "Категория заявки"
        verbose_name_plural = "Категории заявок"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    agreement = models.BooleanField(default=False, verbose_name="Согласие на обработку ПД")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль {self.user.username}"


class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('done', 'Выполнено'),
        ('rejected', 'Отклонена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=200, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    room_type = models.CharField(
        max_length=20,
        choices=[
            ('bedroom', 'Спальня'),
            ('bathroom', 'Ванная'),
            ('kitchen', 'Кухня'),
            ('living_room', 'Гостиная'),
            ('office', 'Офис'),
            ('other', 'Другое'),
        ],
        default='other',
        verbose_name="Тип помещения"
    )
    message = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='request_photos/', verbose_name="Фото помещения или план")
    design_image = models.ImageField(upload_to='design_images/', blank=True, null=True, verbose_name="Изображение готового дизайна")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    designer_comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Комментарий дизайнера",
        help_text="Опишите, что было сделано или какие есть нюансы"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        category_str = f" ({self.category})" if self.category else ""
        return f"Заявка от {self.user.username} на {self.get_room_type_display()}{category_str}"

    def get_absolute_url(self):
        return reverse('request-detail', args=[str(self.id)])


