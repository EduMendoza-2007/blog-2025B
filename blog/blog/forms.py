from django import forms

_INPUT = "w-full rounded-lg bg-black/30 border border-white/10 px-3 py-2 text-white placeholder-white/40 outline-none focus:ring-2 focus:ring-emerald-400"
_TEXTAREA = "w-full min-h-32 rounded-lg bg-black/30 border border-white/10 px-3 py-2 text-white placeholder-white/40 outline-none focus:ring-2 focus:ring-emerald-400"
_CHECK = "h-4 w-4 rounded border-white/20 bg-black/30 text-emerald-500 focus:ring-emerald-400"

class ContactForm(forms.Form):
    name = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Tu nombre",
            "class": _INPUT,
            "id": "id_name",
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "tu@email.com",
            "class": _INPUT,
            "id": "id_email",
        })
    )
    subject = forms.CharField(
        label="Asunto",
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "¿Sobre qué querés hablar?",
            "class": _INPUT,
            "id": "id_subject",
        })
    )
    message = forms.CharField(
        label="Mensaje",
        max_length=2000,
        widget=forms.Textarea(attrs={
            "rows": 6,
            "placeholder": "Contanos en qué podemos ayudarte...",
            "class": _TEXTAREA,
            "id": "id_message",
        })
    )
    consent = forms.BooleanField(
        required=False,
        label="Acepto ser contactad@ por email",
        widget=forms.CheckboxInput(attrs={"class": _CHECK, "id": "id_consent"})
    )
