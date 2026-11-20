from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room, DesignProposal, DesignStyle, Material, Designer, Request, Category


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


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
            'plan_image': 'Загрузите план или фото помещения (JPG, PNG)',
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
        fields = ['category', 'room_type', 'message']
        labels = {
            'category': 'Категория заявки',
            'room_type': 'Тип помещения',
            'message': 'Ваши пожелания к дизайну',
        }
        help_texts = {
            'message': 'Опишите, как вы хотите оформить это помещение: стиль, цвета, материалы и т.д.',
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Название категории',
            'description': 'Описание',
        }