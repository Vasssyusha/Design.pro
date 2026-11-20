from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
    path('room/<uuid:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('room/create/', views.RoomCreate.as_view(), name='room-create'),
    path('room/<uuid:pk>/update/', views.RoomUpdate.as_view(), name='room-update'),
    path('room/<uuid:pk>/delete/', views.RoomDelete.as_view(), name='room-delete'),

    path('proposals/', views.ProposalListView.as_view(), name='proposals'),
    path('proposal/<uuid:pk>/', views.ProposalDetailView.as_view(), name='proposal-detail'),
    path('proposal/create/', views.ProposalCreate.as_view(), name='proposal-create'),
    path('proposal/<uuid:pk>/update/', views.ProposalUpdate.as_view(), name='proposal-update'),
    path('proposal/<uuid:pk>/delete/', views.ProposalDelete.as_view(), name='proposal-delete'),

    path('all-rooms/', views.AllRoomsListView.as_view(), name='all-rooms'),
    path('register/', views.register, name='register'),
]