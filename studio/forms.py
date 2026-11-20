from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room, DesignProposal


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
        fields = ['title', 'description', 'style', 'materials', 'preview_image']
        labels = {
            'title': 'Название варианта',
            'description': 'Описание варианта',
            'style': 'Стиль оформления',
            'materials': 'Материалы',
            'preview_image': 'Изображение варианта',
        }