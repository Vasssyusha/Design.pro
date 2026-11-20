from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Room, DesignProposal, DesignStyle, Material, Designer


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
    list_display = ('title', 'room_type', 'style', 'created_at')
    list_filter = ('style', 'room_type', 'created_at')
    search_fields = ('title',)


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'experience_years', 'phone')
    list_filter = ('experience_years',)
    search_fields = ('first_name', 'last_name', 'phone')


class CustomUserAdmin(BaseUserAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return (
            (None, {'fields': ('username',)}),
            ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
            ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        )
    readonly_fields = ()


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)