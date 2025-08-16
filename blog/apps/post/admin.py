from django.contrib import admin
from apps.post.models import Post, PostImage, Category, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "post_count")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

    def post_count(self, obj):
        # Ajusta el related_name si en tu modelo Post usaste otro
        return obj.post_set.count()
    post_count.short_description = "Posts"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "allow_comments", "created_at", "updated_at")
    search_fields = ("id", "title", "content", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("category", "author", "created_at", "allow_comments")
    ordering = ("-created_at",)
    list_select_related = ("author", "category")
    date_hierarchy = "created_at"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "created_at")
    search_fields = ("id", "author__username", "post__title")
    list_filter = ("created_at", "author")
    ordering = ("-created_at",)
    list_select_related = ("author", "post")

def activate_images(modeladmin, request, queryset):
    updated = queryset.update(active=True)
    modeladmin.message_user(request, f"{updated} imágenes fueron activadas correctamente")
activate_images.short_description = "Activar imágenes seleccionadas"

def deactivate_images(modeladmin, request, queryset):
    updated = queryset.update(active=False)  # <-- ahora sí desactiva
    modeladmin.message_user(request, f"{updated} imágenes fueron desactivadas correctamente")
deactivate_images.short_description = "Desactivar imágenes seleccionadas"

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ("post", "image", "active", "created_at")
    # Buscar por el post es suficiente; ImageField no siempre rinde en search_fields
    search_fields = ("post__id", "post__title")
    list_filter = ("active",)
    actions = [activate_images, deactivate_images]
    list_select_related = ("post",)
