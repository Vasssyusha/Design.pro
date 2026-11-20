from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Комнаты (id = UUID)
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
    path('room/<uuid:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('room/create/', views.RoomCreate.as_view(), name='room-create'),
    path('room/<uuid:pk>/update/', views.RoomUpdate.as_view(), name='room-update'),
    path('room/<uuid:pk>/delete/', views.RoomDelete.as_view(), name='room-delete'),

    # Предложения (id = int)
    path('proposals/', views.ProposalListView.as_view(), name='proposals'),
    path('proposal/<int:pk>/', views.ProposalDetailView.as_view(), name='proposal-detail'),
    path('proposal/create/', views.ProposalCreate.as_view(), name='proposal-create'),
    path('proposal/<int:pk>/update/', views.ProposalUpdate.as_view(), name='proposal-update'),
    path('proposal/<int:pk>/delete/', views.ProposalDelete.as_view(), name='proposal-delete'),

    # Все комнаты (для дизайнеров)
    path('all-rooms/', views.AllRoomsListView.as_view(), name='all-rooms'),

    # Материалы (id = int)
    path('materials/', views.MaterialListView.as_view(), name='materials'),
    path('material/create/', views.MaterialCreate.as_view(), name='material-create'),
    path('material/<int:pk>/update/', views.MaterialUpdate.as_view(), name='material-update'),
    path('material/<int:pk>/delete/', views.MaterialDelete.as_view(), name='material-delete'),

    # Дизайнеры (id = int)
    path('designers/', views.DesignerListView.as_view(), name='designers'),
    path('designer/<int:pk>/', views.DesignerDetailView.as_view(), name='designer-detail'),
    path('designer/create/', views.DesignerCreate.as_view(), name='designer-create'),
    path('designer/<int:pk>/update/', views.DesignerUpdate.as_view(), name='designer-update'),
    path('designer/<int:pk>/delete/', views.DesignerDelete.as_view(), name='designer-delete'),

    # Регистрация
    path('register/', views.register, name='register'),
]