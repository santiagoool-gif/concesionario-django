from django import forms
from .models import Carro, Caracteristica


class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ["carro_text", "precio", "pub_date","anio"]
        widgets = {
            "carro_text": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: BMW 320i 2020",
            }),
            "precio": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: 85000000",
                "min": "0",
            }),
            "pub_date": forms.DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
            }),
             "anio": forms.NumberInput(attrs={
             "class": "form-control",
                "placeholder": "Ej:  2020",
            }),
        }
        labels = {
            "carro_text": "Vehículo",
            "precio": "Precio",
            "pub_date": "Fecha de publicación",
        }


class CaracteristicaForm(forms.ModelForm):
    caracteristica_text = forms.CharField(
        label="Característica",
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ejemplo: Motor 2.0, Caja automática, Techo panorámico..."
            }
        )
    )

    class Meta:
        model = Caracteristica
        fields = ["caracteristica_text"]