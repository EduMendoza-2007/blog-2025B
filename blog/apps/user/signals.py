from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from apps.post.models import Post, Comment
from apps.user.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def created_groups_and_permissions(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        try:
            post_content_type = ContentType.objects.get_for_model(Post)
            comment_content_type = ContentType.objects.get_for_model(Comment)

            # Permisos de POST  
            view_post_permission = Permission.objects.get(
                codename='view_post',
                content_type=post_content_type
            )
            add_post_permission = Permission.objects.get(
                codename='add_post',
                content_type=post_content_type
            )
            change_post_permission = Permission.objects.get(
                codename='change_post',
                content_type=post_content_type
            )
            delete_post_permission = Permission.objects.get(
                codename='delete_post',
                content_type=post_content_type
            )

            #Permiso de COMMENT
            view_comment_permission = Permission.objects.get(
                codename='view_comment',
                content_type=comment_content_type
            )
            add_comment_permission = Permission.objects.get(
                codename='add_comment',
                content_type=comment_content_type
            )
            change_comment_permission = Permission.objects.get(
                codename='change_comment',
                content_type=comment_content_type
            )
            delete_comment_permission = Permission.objects.get(
                codename='delete_comment',
                content_type=comment_content_type
            )

            #Crear grupo de usuarios registrados
            registered_group, created = Group.objects.get_or_create(
                name='Registereds'
            )
            registered_group.permissions.add(
                view_post_permission,
                change_post_permission,
                delete_post_permission,

                view_comment_permission,
                add_comment_permission,
                change_comment_permission,
                delete_comment_permission
                #Permiso para ver posts
                #Permiso para crear posts
                #Permiso para actualizar sus posts
                #Permiso para borrar sus posts
                #Permiso para ver comentarios de posts
                #Permiso para crear comentarios de un post
                #Permiso para actualizar de su comentario en un post
                #Permiso para borrar su comentario de un post
            )
            
            #Crear grupo de usuarios colaboradores
            registered_group, created = Group.objects.get_or_create(
                name='Collaborators'
            )
            registered_group.permissions.add(
                view_post_permission,
                add_post_permission,
                change_post_permission,
                delete_post_permission,
                view_comment_permission,
                add_comment_permission,
                change_comment_permission,
                delete_comment_permission,
                #Permiso para ver posts
                #Permiso para crear posts
                #Permiso para actualizar sus posts
                #Permiso para borrar sus posts
                #Permiso para ver comentarios de posts
                #Permiso para ver comentarios del post
                #Permiso para crear comentarios de un post
                #Permiso para actualizar de su comentario en un post
                #Permiso para borrar su comentario de un post
            )   
            # #Crear grupos de usuarios administradores
            admin_group, created = Group.objects.get_or_create(
                name='Admins'
            )
            registered_group.permissions.add(
                view_post_permission,
                add_post_permission,
                change_post_permission,
                delete_post_permission,
                view_comment_permission,
                add_comment_permission,
                change_comment_permission,
                delete_comment_permission
            )
            
            print("Grupos y permisos creados correctamente.")
        except ContentType.DoesNotExist:
            print("El tipo aun no se encuentra disponible.")
        except Permission.DoesNotExist:
            print("Uno o mas permisos no existen.")