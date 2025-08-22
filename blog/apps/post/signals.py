# apps/post/signals.py
from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate, dispatch_uid="apps_post_create_roles_perms")
def create_roles_and_perms(sender, **kwargs):
    """
    Crea/actualiza los grupos 'Miembro' y 'Colaborador' con permisos
    basados en los modelos reales: Post, PostImage, Comment, Category.
    Se ejecuta después de migrar la app 'post'.
    """
    # Asegura que esto corra solo cuando migra nuestra app
    if getattr(sender, "label", None) != "post":
        return

    # Obtiene modelos por label 'post' (porque tu AppConfig.name es 'apps.post' y el label por defecto es 'post')
    Post = apps.get_model("post", "Post")
    PostImage = apps.get_model("post", "PostImage")
    Comment = apps.get_model("post", "Comment")
    Category = apps.get_model("post", "Category")

    # ContentTypes
    ct_post = ContentType.objects.get_for_model(Post)
    ct_postimage = ContentType.objects.get_for_model(PostImage)
    ct_comment = ContentType.objects.get_for_model(Comment)
    ct_category = ContentType.objects.get_for_model(Category)

    # Helper para traer permisos "core" que YA existen
    def get_perm(action: str, ct: ContentType) -> Permission:
        # codenames estándar: add_*, change_*, delete_*, view_*
        return Permission.objects.get(codename=f"{action}_{ct.model}", content_type=ct)

    # Crea grupos si no existen
    colaborador, _ = Group.objects.get_or_create(name="Colaborador")
    miembro, _ = Group.objects.get_or_create(name="Miembro")

    # ---- Permisos por grupo ----
    # Miembro: comentar (crear). El control de "editar/eliminar solo los tuyos"
    # se hace en las views (comprobando autor).
    miembro_perms = [
        get_perm("add", ct_comment),
        get_perm("view", ct_post),
        get_perm("view", ct_category),
        get_perm("view", ct_comment),
    ]
    miembro.permissions.set(miembro_perms)

    # Colaborador: CRUD de posts, imágenes, categorías + ver todo + comentar y moderar (change/delete comentarios)
    colaborador_perms = [
        # Post
        get_perm("add", ct_post), get_perm("change", ct_post),
        get_perm("delete", ct_post), get_perm("view", ct_post),

        # PostImage (si administrás imágenes por separado)
        get_perm("add", ct_postimage), get_perm("change", ct_postimage),
        get_perm("delete", ct_postimage), get_perm("view", ct_postimage),

        # Categorías
        get_perm("add", ct_category), get_perm("change", ct_category),
        get_perm("delete", ct_category), get_perm("view", ct_category),

        # Comentarios (incluye moderación por permisos + lógica en views)
        get_perm("add", ct_comment), get_perm("change", ct_comment),
        get_perm("delete", ct_comment), get_perm("view", ct_comment),
    ]
    colaborador.permissions.set(colaborador_perms)
