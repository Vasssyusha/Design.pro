from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from .models import (
    Room, DesignProposal, DesignStyle, Material,
    Designer, Request, Category, Profile,
)

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp']
MAX_IMAGE_SIZE = 2 * 1024 * 1024

def validate_image(file, label):
    ext = file.name.split('.')[-1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Недопустимый формат файла «{label}»: '.{ext}'. "
            f"Разрешены только: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}."
        )

    if file.size > MAX_IMAGE_SIZE:
        size_mb = file.size / (1024 * 1024)
        raise ValidationError(
            f"Размер файла «{label}» {size_mb:.2f} МБ превышает "
            f"допустимый лимит {MAX_IMAGE_SIZE // (1024 * 1024)} МБ."
        )


class CustomUserCreationForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        label="ФИО",
        widget=forms.TextInput(attrs={'placeholder': 'Андреев Андрей Андреевич'}),
    )
    username = forms.CharField(
        max_length=150,
        label="Логин",
        widget=forms.TextInput(attrs={'placeholder': 'andreev-andrey'}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'example@mail.com'}),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
    )
    password2 = forms.CharField(
        label="Повтор пароля",
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
    )
    agreement = forms.BooleanField(
        label="Я согласен на обработку персональных данных",
        required=True,
    )

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if not full_name:
            raise ValidationError("ФИО обязательно для заполнения.")
        if not re.match(r'^[А-Яа-яЁё\s\-]+$', full_name):
            raise ValidationError("ФИО должно содержать только кириллические буквы, дефис и пробелы.")
        if len(full_name.split()) < 2:
            raise ValidationError("ФИО должно содержать минимум имя и фамилию.")
        return full_name

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise ValidationError("Логин обязателен для заполнения.")
        if not re.match(r'^[a-zA-Z\-]+$', username):
            raise ValidationError("Логин должен содержать только латинские буквы и дефис.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise ValidationError("Email обязателен для заполнения.")
        if not re.match(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Введите корректный email-адрес.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        if not password:
            raise ValidationError("Пароль обязателен для заполнения.")
        if len(password) < 6:
            raise ValidationError("Пароль должен содержать минимум 6 символов.")
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if not password2:
            raise ValidationError("Повтор пароля обязателен для заполнения.")
        if password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2

    def clean_agreement(self):
        if not self.cleaned_data.get('agreement', False):
            raise ValidationError("Необходимо дать согласие на обработку персональных данных.")
        return self.cleaned_data['agreement']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['title', 'room_type', 'area', 'description', 'plan_image']
        labels = {
            'title': 'Название помещения',
            'room_type': 'Тип помещения',
            'area': 'Площадь (м²)',
            'description': 'Описание пожеланий',
            'plan_image': 'План помещения',
        }
        help_texts = {
            'plan_image': 'Загрузите план или фото помещения (JPG, PNG).',
        }


class DesignProposalForm(forms.ModelForm):
    class Meta:
        model = DesignProposal
        fields = ['title', 'description', 'style', 'materials', 'preview_image', 'room_type']
        labels = {
            'title': 'Название варианта',
            'description': 'Описание варианта',
            'style': 'Стиль оформления',
            'materials': 'Материалы',
            'preview_image': 'Изображение варианта',
            'room_type': 'Тип помещения',
        }


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'category', 'room_type', 'message', 'photo']
        labels = {
            'title': 'Название',
            'category': 'Категория',
            'room_type': 'Тип помещения',
            'message': 'Описание',
            'photo': 'Фото помещения или его план',
        }
        help_texts = {
            'message': 'Опишите, как вы хотите оформить помещение: стиль, цвета, материалы и т.д.',
            'photo': 'Допустимые форматы: jpg, jpeg, png, bmp. Максимальный размер — 2 МБ.',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Например: Ремонт ванной комнаты'}),
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise ValidationError("Название обязательно для заполнения.")
        return title

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise ValidationError("Выберите категорию из списка.")
        return category

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if not message:
            raise ValidationError("Описание обязательно для заполнения.")
        return message

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            raise ValidationError("Загрузите фото помещения или его план.")
        validate_image(photo, "фото помещения")
        return photo


class RequestStatusForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['status', 'category', 'design_image', 'designer_comment']
        labels = {
            'status': 'Статус',
            'category': 'Категория',
            'design_image': 'Изображение готового дизайна',
            'designer_comment': 'Комментарий дизайнера',
        }
        help_texts = {
            'design_image': 'Обязательно при статусе «Выполнено». Форматы: jpg, jpeg, png, bmp. Макс. 2 МБ.',
            'designer_comment': 'Обязателен при переводе заявки из «Новая» в «Принято в работу».',
        }
        widgets = {
            'designer_comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Например: Принимаю заявку в работу, уточню детали по телефону...',}),
        }

    def __init__(self, *args, **kwargs):
        self.original_status = kwargs.pop('original_status', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        design_image = cleaned_data.get('design_image')
        comment = (cleaned_data.get('designer_comment') or '').strip()
        old = self.original_status

        allowed = {'new': 'in_progress', 'in_progress': 'done'}
        if old in allowed and status != old and status != allowed[old]:
            self.add_error('status', 'Недопустимый переход статуса.')
        if old in ('done', 'rejected') and status != old:
            self.add_error('status', 'Смена статуса невозможна.')

        if old == 'new' and status == 'in_progress' and not comment:
            self.add_error(
                'designer_comment',
                'При переводе заявки в статус «Принято в работу» необходимо указать комментарий.'
            )

        if status == 'done' and not design_image and not self.instance.design_image:
            self.add_error(
                'design_image',
                'При статусе «Выполнено» необходимо прикрепить изображение готового дизайна.'
            )
        elif design_image:
            validate_image(design_image, "изображение готового дизайна")

        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Название категории',
            'description': 'Описание',
        }