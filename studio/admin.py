from django.contrib import admin
from .models import Room, DesignProposal, DesignStyle, Material


@admin.register(DesignStyle)
class DesignStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'room_type', 'status', 'created_at')
    list_filter = ('status', 'room_type', 'created_at')
    search_fields = ('title', 'user__username')


@admin.register(DesignProposal)
class DesignProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'room', 'designer', 'style', 'created_at')
    list_filter = ('style', 'created_at')
    search_fields = ('title', 'room__title', 'designer__username')