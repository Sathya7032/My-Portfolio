from django.contrib import admin
from .models import ContactMessage, Blog


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('is_read',)
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as Read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as Unread"


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'views', 'is_published', 'published_at')
    list_filter = ('is_published', 'category', 'published_at', 'author')
    search_fields = ('title', 'description', 'content', 'tags', 'sources')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'created_at', 'updated_at')
    fieldsets = (
        ("Core Information", {
            'fields': ('title', 'slug', 'author', 'category', 'tags', 'read_time')
        }),
        ("Summary & Media", {
            'fields': ('description', 'image', 'image_url')
        }),
        ("Content & Citations", {
            'fields': ('content', 'sources')
        }),
        ("Status & Publishing", {
            'fields': ('is_published', 'published_at', 'views', 'created_at', 'updated_at')
        }),
    )

    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/tinymce/6.8.3/tinymce.min.js',
            'js/admin_tinymce.js',
        )
        css = {
            'all': ('css/admin_tinymce.css',)
        }
