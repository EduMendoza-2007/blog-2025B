# apps/user/signals.py
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from apps.post.models import Post, Comment
from apps.user.models import User


def _collect_perms():
    """
    Devuelve un diccionario con conjuntos de permisos útiles, ya creados por Django
    (add/change/delete/view) para Post y Comment.
    """
    ct_post = ContentType.objects.get_for_model(Post)
    ct_comment = ContentType.objects.get_for_model(Comment)

    perms_qs = Permission.objects.filter(content_type__in=[ct_post, ct_comment])
    perms = {p.codename: p for p in perms_qs}

    def pick(*codes):
        return [perms[c] for c in codes if c in perms]

    return {
        "post_all": pick("add_post", "change_post", "delete_post", "view_post"),
        "post_create_edit_view": pick("add_post", "change_post", "view_post"),
        "post_view": pick("view_post"),
        "comment_all": pick("add_comment", "change_comment", "delete_comment", "view_comment"),
        "comment_create_edit_view": pick("add_comment", "change_comment", "view_comment"),
        "comment_view": pick("view_comment"),
    }


def _ensure_groups_and_permissions():
    """
    Crea/actualiza grupos y asigna permisos de forma idempotente.
    Mantiene grupos en español y agrega alias en inglés para compatibilidad.
    """
    try:
        sets = _collect_perms()
    except Exception:
        # Puede fallar en la primera corrida si aún no existen ContentTypes/Permissions
        return

    # ---- Grupos en español
    admins, _ = Group.objects.get_or_create(name="Admins")
    editores, _ = Group.objects.get_or_create(name="Editores")
    colaboradores, _ = Group.objects.get_or_create(name="Colaboradores")
    visitantes, _ = Group.objects.get_or_create(name="Visitantes")

    # ---- Alias/compatibilidad en inglés
    registered, _ = Group.objects.get_or_create(name="Registered")
    collaborators_alias, _ = Group.objects.get_or_create(name="Collaborators")

    # Asignación de permisos (puedes ajustar a tu política real)
    admins.permissions.set(sets["post_all"] + sets["comment_all"])

    # Editores: full sobre Post y Comment (como en tu segundo bloque)
    editores.permissions.set(sets["post_all"] + sets["comment_all"])

    # Colaboradores: pueden crear/editar/ver Post; y full en Comment (como tu primer bloque)
    colaboradores.permissions.set(sets["post_create_edit_view"] + sets["comment_all"])

    # Visitantes: ver Post (opcionalmente pueden ver Comment si tu lógica lo requiere)
    visitantes.permissions.set(sets["post_view"])  # agrega + sets["comment_view"] si quieres

    # Registered (alias práctico de “usuario registrado”):
    # ver Post + operar en Comment (como en tu primer bloque)
    registered.permissions.set(sets["post_view"] + sets["comment_all"])

    # Collaborators (alias de Colaboradores)
    collaborators_alias.permissions.set(sets["post_create_edit_view"] + sets["comment_all"])


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Se ejecuta después de `migrate` para garantizar grupos y permisos.
    """
    _ensure_groups_and_permissions()


@receiver(post_save, sender=User)
def assign_groups_on_user_create(sender, instance, created, **kwargs):
    """
    Al crear usuarios:
    - Superusuario -> Admins
    - Usuario normal -> Registered
    (Si el grupo aún no existe porque no corriste migrate, no rompe.)
    """
    if not created:
        return
    try:
        if instance.is_superuser:
            g = Group.objects.get(name="Admins")
        else:
            g = Group.objects.get(name="Registered")
        instance.groups.add(g)
    except Group.DoesNotExist:
        # Si aún no existen los grupos, no interrumpe el alta del usuario
        pass
