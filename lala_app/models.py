# lala_app/models.py
from django.db import models
from django.contrib.auth.models import User

# lala_app/models.py
class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    direccion = models.TextField(blank=True, null=True)  # Nuevo campo
    fecha_registro = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.get_full_name()}"

# ... resto de los modelos

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    direccion = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='clientes/', blank=True, null=True)  # Nuevo campo
    fecha_registro = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.usuario.get_full_name()}"

class Empleado(models.Model):
    nombre = models.CharField(max_length=200)
    puesto = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_contratacion = models.DateField()
    horas_semanales = models.IntegerField()
    foto = models.ImageField(upload_to='empleados/')
    
    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    telefono = models.CharField(max_length=15)
    empresa = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200)
    email = models.EmailField()
    direccion = models.TextField()
    categoria = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='proveedores/')
    
    def __str__(self):
        return self.empresa

class Resena(models.Model):
    ESTRELLAS = [
        (1, '1 Estrella'),
        (2, '2 Estrellas'),
        (3, '3 Estrellas'),
        (4, '4 Estrellas'),
        (5, '5 Estrellas'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descripcion = models.TextField()
    calificacion = models.IntegerField(choices=ESTRELLAS)
    foto_producto = models.ImageField(upload_to='resenas/', blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Reseña de {self.cliente} para {self.producto}"

class Receta(models.Model):
    nombre = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='recetas/')
    descripcion = models.TextField()
    ingredientes = models.TextField()
    
    def __str__(self):
        return self.nombre

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    completada = models.BooleanField(default=False)  # ← ESTE CAMPO DEBE EXISTIR

    def save(self, *args, **kwargs):
        # Forzar a booleano si hay problema
        self.completada = bool(self.completada)
        super().save(*args, **kwargs)
    
    # AGREGAR ESTE CAMPO si no existe
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', '⏳ Pendiente'),
            ('completado', '✅ Completado'),
        ],
        default='pendiente'
    )
    
    # O si ya tienes 'completada', mantenlo así:
    completada = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.usuario.username}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Detalle {self.id} - Venta {self.venta.id}"
    
