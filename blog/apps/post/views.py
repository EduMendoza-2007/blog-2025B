# apps/post/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Count, Q
from django.db import transaction
from django.conf import settings
from apps.post.forms import PostFilterForm, PostCreateForm, CommentForm, PostForm, PostUpdateForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from apps.post.models import Post, PostImage, Comment
from apps.post.forms import PostFilterForm, PostCreateForm, CommentForm, PostForm


def is_moderator(user) -> bool:
    """Colaborador o Superadmin."""
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name="Colaborador").exists() or user.has_perm("post.change_comment")


class PostListView(ListView):
    model = Post
    template_name = "post/post_list.html"
    context_object_name = "posts"
    paginate_by = 10  # antes estaba en 1; subilo a conveniencia

    def get_queryset(self):
        qs = (
            Post.objects.all()
            .select_related("author", "category")
            .prefetch_related("images")
            .annotate(comments_count=Count("comments"))
        )

        search_query = (self.request.GET.get("search_query") or "").strip()
        order_by = self.request.GET.get("order_by") or "-created_at"

        if search_query:
            qs = qs.filter(
                Q(title__icontains=search_query)
                | Q(content__icontains=search_query)
                | Q(author__username__icontains=search_query)
                | Q(category__title__icontains=search_query)
            )

        allowed_orders = {"-created_at", "created_at", "-comments_count"}
        if order_by not in allowed_orders:
            order_by = "-created_at"

        return qs.order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = PostFilterForm(self.request.GET)

        if context.get("is_paginated", False):
            query_params = self.request.GET.copy()
            query_params.pop("page", None)

            pagination = {}
            page_obj = context["page_obj"]
            paginator = context["paginator"]

            base = f"?{query_params.urlencode()}" if query_params else "?"

            if page_obj.number > 1:
                pagination["first_page"] = f"{base}page=1"

            if page_obj.has_previous():
                pagination["previous_page"] = f"{base}page={page_obj.number - 1}"

            if page_obj.has_next():
                pagination["next_page"] = f"{base}page={page_obj.number + 1}"

            if page_obj.number < paginator.num_pages:
                pagination["last_page"] = f"{base}page={paginator.num_pages}"

            context["pagination"] = pagination

        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "post/post_create.html"
    permission_required = "post.add_post"

    @transaction.atomic
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        if images:
            for image in images:
                PostImage.objects.create(post=self.object, image=image)
        else:
            PostImage.objects.create(post=self.object, image=settings.DEFAULT_POST_IMAGE)
        return response

    def get_success_url(self):
        return reverse("post:post_detail", kwargs={"slug": self.object.slug})



class PostDetailView(DetailView):
    model = Post
    template_name = "post/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post: Post = self.object
        context["active_images"] = post.images.filter(active=True)

        
        if self.request.user.is_authenticated and self.request.user.has_perm("post.add_comment") and post.allow_comments:
            context["add_comment_form"] = CommentForm()

        
        edit_comment_id = self.request.GET.get("edit_comment")
        if edit_comment_id and self.request.user.is_authenticated:
            comment = get_object_or_404(Comment, id=edit_comment_id, post=post)
            if comment.author_id == self.request.user.id or is_moderator(self.request.user):
                context["editing_comment_id"] = comment.id
                context["edit_comment_form"] = CommentForm(instance=comment)

        
        delete_comment_id = self.request.GET.get("delete_comment")
        if delete_comment_id and self.request.user.is_authenticated:
            comment = get_object_or_404(Comment, id=delete_comment_id, post=post)
            if comment.author_id == self.request.user.id or is_moderator(self.request.user):
                context["deleting_comment_id"] = comment.id

        return context


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'post/post_update.html'
    
    def test_func(self):
        post = self.get_object()
        return (self.request.user == post.author and self.request.user.is_collaborator) or self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_admin

    #def get_form(self, form_class=None):
    #    form = super().get_form(form_class)
    #    form.fields['image'].initial = self.object.images.filter(active=True).first()
    #    return form

    #def form_valid(self, form):
    #    ifs
    #    mantener imagenes avtivas
    #    agregar nuevas imagenes
    #    no agrega ni mantiene imagenes
    #    guardar post post.save()

    #   return super().form_valid()

    def get_success_url(self):
        return reverse_lazy("post:post_detail", kwargs={"slug": self.object.slug})


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "post/post_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    permission_required = "post.delete_post"
    success_url = reverse_lazy("post:post_list")

    def test_func(self):
        post = self.get_object()
        return (self.request.user == post.author and self.request.user.is_collaborator) or self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_admin

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'Eliminar "{self.object.title}"'
        return context




class CommentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "post/post_detail.html"
    permission_required = "post.add_comment"

    def dispatch(self, request, *args, **kwargs):
        
        self.post_obj = get_object_or_404(Post, slug=self.kwargs["slug"])
        if not self.post_obj.allow_comments:
            messages.error(request, "Los comentarios están deshabilitados en este post.")
            return redirect(self.post_obj.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        messages.success(self.request, "¡Comentario publicado!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post:post_detail", kwargs={"slug": self.object.post.slug})


class CommentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'post_detail'
    
    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug})
    
    def test_func(self):
        comment = self.get_object()
        # dueño o moderador
        return self.request.user.id == comment.author_id or is_moderator(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Comentario actualizado.")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Comentario'
        context['post'] = self.object.post
        return context


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse_lazy('post:post_detail', kwargs={'slug': self.object.post.slug})
    
    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['pk'])

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author