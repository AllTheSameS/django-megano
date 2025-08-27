from django.contrib import admin
from django.utils.html import format_html

from .models import Profile, Avatar


class AvatarInline(admin.StackedInline):
    model = Avatar
    extra = 0
    max_num = 1
    can_delete = False
    verbose_name = 'Аватар'
    verbose_name_plural = 'Аватар'
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        if obj.src:
            return format_html('<img src="{}" height="100" style="border-radius: 50%;" />', obj.src.url)
        return "Аватар не установлен"
    avatar_preview.short_description = 'Превью'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'email', 'balance', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'full_name', 'phone', 'email')
    readonly_fields = ('user', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'full_name')
        }),
        ('Контактные данные', {
            'fields': ('phone', 'email')
        }),
        ('Финансы', {
            'fields': ('balance',),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [AvatarInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ('profile', 'alt', 'avatar_preview')
    search_fields = ('profile__user__username', 'profile__full_name', 'alt')
    list_select_related = ('profile__user',)
    readonly_fields = ('avatar_preview',)

    def avatar_preview(self, obj):
        if obj.src:
            return format_html('<img src="{}" height="150" style="border-radius: 50%;" />', obj.src.url)
        return "Аватар не установлен"
    avatar_preview.short_description = 'Превью'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile__user')
