from django import forms
from apps.post.models import Category, Comment, Post, PostImage

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'allow_comments')

class PostCreateForm(PostForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Selecciona una categoría",
        widget=forms.Select(attrs={'class': 'w-full p-2'})
    )
    image = forms.ImageField(required=False)

    def save(self, commit=True):
        post = super().save(commit=False)
        image = self.cleaned_data['image']
        category = self.cleaned_data['category']

        post.category = category

        if  commit:
            post.save()
            if image:
                PostImage.objects.create(post=post, image=image)

        return post

from django import forms
from .models import Post, PostImage


class PostUpdateForm(PostForm):
    image = forms.ImageField(required=False)
    
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        # Crear checkboxes para imágenes existentes
        if self.instance and self.instance.pk:
            for img in PostImage.objects.filter(post=self.instance):
                self.fields[f"keep_image_{img.id}"] = forms.BooleanField(
                    required=False,
                    initial=True,
                    label=f"Mantener imagen"
                )

    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
            
            # Eliminar imágenes no marcadas
            if post.pk:
                for img in PostImage.objects.filter(post=post):
                    keep = self.cleaned_data.get(f"keep_image_{img.id}", False)
                    if not keep:
                        img.delete()
            
            # Agregar nueva imagen
            if self.cleaned_data.get('image'):
                PostImage.objects.create(
                    post=post, 
                    image=self.cleaned_data['image']
                )
        
        return post

class PostFilterForm(forms.Form):
    search_query = forms.CharField(
    required=False, 
    widget=forms.TextInput(
        attrs={'placeholder': 'Buscar...', 'class': 'w-full p-2 bg-red-200'}
        )
    )
    order_by = forms.ChoiceField(
        required=False,
        choices=(
            ('-created_at', 'Mas recientes'),
            ('created_at', 'Mas antiguos'),
            ('-comments_count', 'Mas comentados'),
        ),
        widget=forms.Select(
            attrs={'class': 'w-full p-2'}
        )
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Comentario'
        }
        widget = {
            'content': forms.Textarea(
                attrs={
                    'rows': 3, 'placeholder': 'Escribe tu comentario...', 'class': 'p-2'
                }
            )
        }