# lala_app/admin.py
from django.contrib import admin
from .models import *

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'categoria']
    list_filter = ['categoria']
    search_fields = ['nombre']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'telefono', 'correo', 'fecha_registro']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name']

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'puesto', 'salario', 'fecha_contratacion']
    search_fields = ['nombre']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['empresa', 'contacto', 'email', 'categoria']
    search_fields = ['empresa', 'contacto']

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'producto', 'calificacion', 'fecha']
    list_filter = ['calificacion', 'fecha']
    search_fields = ['cliente__usuario__username', 'producto__nombre']

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'total', 'cliente']
    list_filter = ['fecha']
    search_fields = ['cliente__usuario__username']

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['venta', 'producto', 'cantidad', 'precio']
    list_filter = ['venta__fecha']