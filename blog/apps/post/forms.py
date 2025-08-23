from django import forms
from apps.post.models import Category, Comment, Post, PostImage


TAILWIND_INPUT = "w-full rounded-lg border border-white/10 bg-white/5 backdrop-blur p-2 text-sm text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-emerald-400/60"
TAILWIND_SELECT = "w-full rounded-lg border border-white/10 bg-white/5 backdrop-blur p-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-400/60"
TAILWIND_TEXTAREA = "w-full rounded-lg border border-white/10 bg-white/5 backdrop-blur p-3 text-sm text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-emerald-400/60"

ALLOWED_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMAGE_MB = 5  

def _validate_image(f):
    if not f:
        return
    
    size_mb = f.size / (1024 * 1024)
    if size_mb > MAX_IMAGE_MB:
        raise ValidationError(f"La imagen supera {MAX_IMAGE_MB} MB (tiene {size_mb:.1f} MB).")
    
    name = f.name.lower()
    if "." not in name or name[name.rfind("."):] not in ALLOWED_IMAGE_EXTS:
        raise ValidationError("Formato no permitido. Usa JPG, PNG o WEBP.")


class TailwindModelForm(forms.ModelForm):
    """Aplica clases Tailwind por defecto en inputs/selects/textarea."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            w = field.widget
            if isinstance(w, forms.Textarea):
                w.attrs.setdefault("class", TAILWIND_TEXTAREA)
            elif isinstance(w, (forms.Select, forms.SelectMultiple)):
                w.attrs.setdefault("class", TAILWIND_SELECT)
            else:
                w.attrs.setdefault("class", TAILWIND_INPUT)


class PostForm(TailwindModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "allow_comments", "category")
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Título del post",
                "maxlength": 200,
            }),
            "content": forms.Textarea(attrs={
                "rows": 8,
                "placeholder": "Escribe el contenido del post… (máx. 10.000 caracteres)",
            }),
        }

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        # Colapsa espacios dobles
        title = " ".join(title.split())
        if not title:
            raise ValidationError("El título no puede estar vacío.")
        return title

    def clean_content(self):
        content = (self.cleaned_data.get("content") or "").strip()
        if not content:
            raise ValidationError("El contenido no puede estar vacío.")
        return content

class PostCreateForm(PostForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Selecciona una categoría",
        widget=forms.Select(attrs={'class': 'w-full p-2 text-green-500'})
    )
    images = forms.ImageField(required=False)

    def save(self, commit=True):
        post = super().save(commit=False)

        post.category = self.cleaned_data['category']

        if commit:
            post.save()

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
        widget=forms.TextInput(attrs={
            "placeholder": "Buscar por título o contenido…",
            "class": TAILWIND_INPUT
        })
    )
    ORDER_CHOICES = (
        ("-created_at", "Más recientes"),
        ("created_at", "Más antiguos"),
        ("-comments_count", "Más comentados"),
        # Si luego anotás rating o views, añadilos acá
        # ("-rating", "Mejor puntuación"),
    )
    order_by = forms.ChoiceField(
        required=False,
        choices=ORDER_CHOICES,
        widget=forms.Select(attrs={"class": TAILWIND_SELECT})
    )

class CommentForm(TailwindModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": "Comentario"}
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Escribe tu comentario…",
                "class": TAILWIND_TEXTAREA
            })
        }

    def clean_content(self):
        content = (self.cleaned_data.get("content") or "").strip()
        
        if len(content) < 2:
            raise ValidationError("El comentario es demasiado corto.")
        if len(content) > 400:
            raise ValidationError("El comentario excede 400 caracteres.")
        return " ".join(content.split())
