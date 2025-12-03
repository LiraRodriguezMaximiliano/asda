# lala_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

# lala_app/forms.py
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'foto', 'categoria']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descripción del producto...'}),
            'precio': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del producto...'}),
        }
        labels = {
            'foto': 'Imagen del Producto',
            'categoria': 'Categoría'
        }

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'puesto', 'salario', 'fecha_contratacion', 'horas_semanales', 'foto']
        widgets = {
            'fecha_contratacion': forms.DateInput(attrs={'type': 'date'}),
            'salario': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'horas_semanales': forms.NumberInput(attrs={'min': '0', 'max': '80'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo del empleado...'}),
            'puesto': forms.TextInput(attrs={'placeholder': 'Puesto de trabajo...'}),
        }
        labels = {
            'foto': 'Foto del Empleado',
            'fecha_contratacion': 'Fecha de Contratación',
            'horas_semanales': 'Horas Semanales'
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['empresa', 'contacto', 'telefono', 'email', 'direccion', 'categoria', 'foto']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Dirección completa...'}),
            'empresa': forms.TextInput(attrs={'placeholder': 'Nombre de la empresa...'}),
            'contacto': forms.TextInput(attrs={'placeholder': 'Persona de contacto...'}),
            'email': forms.EmailInput(attrs={'placeholder': 'correo@empresa.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Número de teléfono...'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Tipo de productos que provee...'}),
        }
        labels = {
            'foto': 'Logo del Proveedor'
        }

# lala_app/forms.py - Asegúrate de tener este form
# lala_app/forms.py
class ResenaForm(forms.ModelForm):
    calificacion = forms.IntegerField(
        widget=forms.HiddenInput(),
        min_value=1,
        max_value=5
    )
    
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Comparte tu experiencia con este producto...'
        }),
        label='Tu Reseña',
        required=True
    )
    
    foto_producto = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        }),
        label='Foto del Producto (opcional)'
    )
    
    class Meta:
        model = Resena
        fields = ['calificacion', 'descripcion', 'foto_producto']
        
class ClienteRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'})
    )
    first_name = forms.CharField(
        required=True, 
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'})
    )
    last_name = forms.CharField(
        required=True, 
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'})
    )
    telefono = forms.CharField(
        required=True, 
        max_length=15, 
        label='Teléfono',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '55 1234 5678'})
    )
    direccion = forms.CharField(
        required=True, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tu dirección completa'}), 
        label='Dirección'
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'telefono', 'direccion', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Cliente.objects.create(
                usuario=user,
                telefono=self.cleaned_data['telefono'],
                correo=self.cleaned_data['email'],
                direccion=self.cleaned_data['direccion']
            )
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario o Correo')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    # lala_app/forms.py - Agregar este form
class PagoForm(forms.Form):
    TARJETAS_ACEPTADAS = [
        ('VISA', 'VISA'),
        ('MC', 'MasterCard'),
        ('AMEX', 'American Express'),
    ]
    
    nombre_titular = forms.CharField(
        max_length=100,
        label='Nombre del Titular',
        widget=forms.TextInput(attrs={'placeholder': 'Como aparece en la tarjeta'})
    )
    numero_tarjeta = forms.CharField(
        max_length=19,
        label='Número de Tarjeta',
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'})
    )
    tipo_tarjeta = forms.ChoiceField(
        choices=TARJETAS_ACEPTADAS,
        label='Tipo de Tarjeta'
    )
    mes_expiracion = forms.ChoiceField(
        choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)],
        label='Mes de Expiración'
    )
    año_expiracion = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(2024, 2035)],
        label='Año de Expiración'
    )
    cvv = forms.CharField(
        max_length=4,
        label='CVV',
        widget=forms.TextInput(attrs={'placeholder': '123', 'maxlength': '4'})
    )
    
    def clean_numero_tarjeta(self):
        numero = self.cleaned_data['numero_tarjeta'].replace(' ', '')
        if not numero.isdigit():
            raise forms.ValidationError('El número de tarjeta solo debe contener dígitos')
        if len(numero) not in [15, 16]:
            raise forms.ValidationError('El número de tarjeta debe tener 15 o 16 dígitos')
        return numero
    
    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not cvv.isdigit():
            raise forms.ValidationError('El CVV solo debe contener dígitos')
        if len(cvv) not in [3, 4]:
            raise forms.ValidationError('El CVV debe tener 3 o 4 dígitos')
        return cvv
    
    def clean(self):
        cleaned_data = super().clean()
        mes = cleaned_data.get('mes_expiracion')
        año = cleaned_data.get('año_expiracion')
        
        if mes and año:
            # Verificar si la tarjeta está expirada
            from datetime import datetime
            ahora = datetime.now()
            mes_actual = ahora.month
            año_actual = ahora.year
            
            if int(año) < año_actual or (int(año) == año_actual and int(mes) < mes_actual):
                raise forms.ValidationError('La tarjeta está expirada')
        
        return cleaned_data
    
class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'foto', 'descripcion', 'ingredientes']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descripción de la receta...'}),
            'ingredientes': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Lista de ingredientes...'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la receta...'}),
        }
        labels = {
            'foto': 'Imagen de la Receta'
        }

class ResenaForm(forms.ModelForm):
    calificacion = forms.IntegerField(
        widget=forms.HiddenInput(),
        min_value=1,
        max_value=5
    )
    
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Comparte tu experiencia con este producto...'
        }),
        label='Tu Reseña',
        required=True
    )
    
    foto_producto = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        }),
        label='Foto del Producto (opcional)'
    )
    
    class Meta:
        model = Resena
        fields = ['calificacion', 'descripcion', 'foto_producto']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['completada']  # Solo el campo que quieres editar
        widgets = {
            'completada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'completada': '¿Pedido Completado?',
        }