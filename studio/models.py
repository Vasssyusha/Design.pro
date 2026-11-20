import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='rooms'
    )
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
    description = models.TextField(
        blank=True,
        verbose_name="Описание пожеланий",
        help_text="Опишите, как вы хотите оформить это помещение"
    )
    plan_image = models.ImageField(
        upload_to='room_plans/',
        verbose_name="План помещения",
        help_text="Загрузите план или фото помещения"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    STATUS_CHOICES = (
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('done', 'Готово'),
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"
        permissions = (("can_make_proposal", "Предлагать варианты оформления"),)

    def get_absolute_url(self):
        return reverse('room-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class DesignProposal(models.Model): #хзхз
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='proposals',
        verbose_name="Помещение"
    )
    designer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Дизайнер",
        related_name='proposals'
    )
    title = models.CharField(max_length=200, verbose_name="Название варианта")
    description = models.TextField(verbose_name="Описание варианта")
    style = models.ForeignKey(
        DesignStyle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Стиль"
    )
    materials = models.ManyToManyField(
        Material,
        blank=True,
        verbose_name="Материалы"
    )
    preview_image = models.ImageField(
        upload_to='proposals/',
        blank=True,
        verbose_name="Изображение варианта"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Предложение по оформлению"
        verbose_name_plural = "Предложения по оформлению"

    def get_absolute_url(self):
        return reverse('proposal-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.title} для {self.room.title}"