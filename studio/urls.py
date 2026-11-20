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
    path('proposal/<int:pk>/', views.ProposalDetailView.as_view(), name='proposal-detail'),
    path('proposal/create/', views.ProposalCreate.as_view(), name='proposal-create'),
    path('proposal/<int:pk>/update/', views.ProposalUpdate.as_view(), name='proposal-update'),
    path('proposal/<int:pk>/delete/', views.ProposalDelete.as_view(), name='proposal-delete'),

    path('all-rooms/', views.AllRoomsListView.as_view(), name='all-rooms'),

    path('materials/', views.MaterialListView.as_view(), name='materials'),
    path('material/create/', views.MaterialCreate.as_view(), name='material-create'),
    path('material/<int:pk>/update/', views.MaterialUpdate.as_view(), name='material-update'),
    path('material/<int:pk>/delete/', views.MaterialDelete.as_view(), name='material-delete'),

    path('designers/', views.DesignerListView.as_view(), name='designers'),
    path('designer/<int:pk>/', views.DesignerDetailView.as_view(), name='designer-detail'),
    path('designer/create/', views.DesignerCreate.as_view(), name='designer-create'),
    path('designer/<int:pk>/update/', views.DesignerUpdate.as_view(), name='designer-update'),
    path('designer/<int:pk>/delete/', views.DesignerDelete.as_view(), name='designer-delete'),

    path('register/', views.register, name='register'),

    path('request/create/', views.RequestCreate.as_view(), name='request-create'),
    path('my-requests/', views.RequestListView.as_view(), name='my-requests'),
    path('request/<int:pk>/', views.RequestDetailView.as_view(), name='request-detail'),
    path('request/<int:pk>/delete/', views.RequestDelete.as_view(), name='request-delete'),
    path('all-requests/', views.AllRequestsListView.as_view(), name='all-requests'),

    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('category/create/', views.CategoryCreate.as_view(), name='category-create'),
    path('category/<int:pk>/update/', views.CategoryUpdate.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category-delete'),

    path('category/<int:pk>/delete/', views.CategoryDelete.as_view(), name='category-delete'),
    path('request/<int:pk>/status/', views.RequestStatusUpdate.as_view(), name='request-status-update'),

    path('accounts/login/', views.custom_login, name='login'),
    path('user-cabinet/', views.user_cabinet, name='user-cabinet'),
    path('admin-cabinet/', views.admin_cabinet, name='admin-cabinet'),
]