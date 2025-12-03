# lala_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from .forms import *


class VentaAdminForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['completada']  # Solo este campo
        widgets = {
            'completada': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'width: 20px; height: 20px;'
            }),
        }
        labels = {
            'completada': 'Marcar como COMPLETADO',
        }
def es_gerente(user):
    return user.groups.filter(name='Gerente').exists()

def index(request):
    # Mostrar algunos productos destacados en la página principal
    productos_destacados = Producto.objects.all()[:6]
    return render(request, 'lala_app/index.html', {'productos_destacados': productos_destacados})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if es_gerente(user):
                return redirect('admin_panel')
            else:
                # Redirigir a la página anterior o al índice
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'lala_app/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cliente.objects.create(usuario=user)
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'lala_app/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

# Quitar @login_required para que cualquiera pueda ver los productos
def productos_lacteos(request):
    productos = Producto.objects.filter(categoria__nombre='Lácteos')
    return render(request, 'lala_app/productos_lacteos.html', {'productos': productos})

# Quitar @login_required para que cualquiera pueda ver los productos
def productos_no_lacteos(request):
    productos = Producto.objects.filter(categoria__nombre='No Lácteos')
    return render(request, 'lala_app/productos_no_lacteos.html', {'productos': productos})

# Quitar @login_required para que cualquiera pueda ver las recetas
def recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'lala_app/recetas.html', {'recetas': recetas})



# Quitar @login_required para que cualquiera pueda ver las reseñas
# lala_app/views.py - Agregar estas funciones

# lala_app/views.py
from django.db.models import Avg

def resenas(request):
    # Obtener todas las reseñas con información del producto y cliente
    reseñas = Resena.objects.select_related('producto', 'cliente__usuario').all().order_by('-fecha')
    
    # Calcular promedios por producto
    productos_con_resenas = Producto.objects.filter(resena__isnull=False).distinct()
    productos_info = []
    
    for producto in productos_con_resenas:
        reseñas_producto = Resena.objects.filter(producto=producto)
        promedio = reseñas_producto.aggregate(Avg('calificacion'))['calificacion__avg'] or 0
        productos_info.append({
            'producto': producto,
            'promedio': round(promedio, 1),
            'total_resenas': reseñas_producto.count()
        })
    
    # Ordenar productos por calificación promedio (mejores primero)
    productos_info.sort(key=lambda x: x['promedio'], reverse=True)
    
    context = {
        'reseñas': reseñas,
        'productos_info': productos_info,
        'productos_con_resenas': productos_con_resenas,
    }
    return render(request, 'lala_app/resenas.html', context)

# lala_app/views.py - Asegúrate de tener esta vista
# lala_app/views.py
@login_required
def agregar_resena(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    try:
        cliente = Cliente.objects.get(usuario=request.user)
    except Cliente.DoesNotExist:
        messages.error(request, 'No se encontró tu perfil de cliente')
        return redirect('detalle_producto', producto_id=producto_id)
    
    # Verificar si ya existe una reseña
    reseña_existente = Resena.objects.filter(cliente=cliente, producto=producto).first()
    
    if request.method == 'POST':
        print("📝 Formulario recibido")  # Debug
        print("Datos POST:", request.POST)  # Debug
        print("Archivos FILES:", request.FILES)  # Debug
        
        form = ResenaForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("✅ Formulario válido")  # Debug
            try:
                if reseña_existente:
                    # Actualizar reseña existente
                    reseña_existente.calificacion = form.cleaned_data['calificacion']
                    reseña_existente.descripcion = form.cleaned_data['descripcion']
                    if 'foto_producto' in request.FILES:
                        reseña_existente.foto_producto = request.FILES['foto_producto']
                    reseña_existente.save()
                    messages.success(request, '¡Reseña actualizada exitosamente!')
                    print("🔄 Reseña actualizada")  # Debug
                else:
                    # Crear nueva reseña
                    reseña = form.save(commit=False)
                    reseña.cliente = cliente
                    reseña.producto = producto
                    reseña.save()
                    messages.success(request, '¡Reseña agregada exitosamente!')
                    print("✅ Nueva reseña creada")  # Debug
                
                return redirect('detalle_producto', producto_id=producto_id)
                
            except Exception as e:
                print("❌ Error al guardar:", str(e))  # Debug
                messages.error(request, f'Error al guardar la reseña: {str(e)}')
        else:
            print("❌ Formulario inválido")  # Debug
            print("Errores:", form.errors)  # Debug
            messages.error(request, 'Por favor corrige los errores en el formulario')
    
    else:
        # GET request - cargar formulario
        if reseña_existente:
            form = ResenaForm(instance=reseña_existente)
        else:
            form = ResenaForm(initial={'calificacion': 5})
    
    context = {
        'form': form,
        'producto': producto,
        'reseña_existente': reseña_existente,
    }
    
    return render(request, 'lala_app/agregar_resena.html', context)
# Mantener @login_required para el carrito y perfil
# lala_app/views.py
@login_required
def carrito(request):
    carrito = request.session.get('carrito', {})
    total = 0
    items = []
    
    for producto_id, item in carrito.items():
        item_total = float(item['precio']) * item['cantidad']
        total += item_total
        items.append({
            'id': producto_id,
            'nombre': item['nombre'],
            'precio': item['precio'],
            'cantidad': item['cantidad'],
            'total': item_total,
            'foto': item.get('foto', '')
        })
    
    context = {
        'items_carrito': items,
        'total_carrito': total,
        'subtotal': total,  # Mismo que total_carrito sin IVA
    }
    
    return render(request, 'lala_app/carrito.html', context)

@login_required
def actualizar_carrito(request, producto_id):
    if request.method == 'POST':
        accion = request.POST.get('accion')
        carrito = request.session.get('carrito', {})
        producto_id_str = str(producto_id)
        
        if producto_id_str in carrito:
            if accion == 'incrementar':
                carrito[producto_id_str]['cantidad'] += 1
            elif accion == 'decrementar':
                carrito[producto_id_str]['cantidad'] -= 1
                if carrito[producto_id_str]['cantidad'] <= 0:
                    del carrito[producto_id_str]
                    messages.success(request, 'Producto eliminado del carrito')
                else:
                    messages.success(request, 'Carrito actualizado')
            elif accion == 'eliminar':
                del carrito[producto_id_str]
                messages.success(request, 'Producto eliminado del carrito')
        
        request.session['carrito'] = carrito
        request.session.modified = True
    
    return redirect('carrito')

@login_required
def vaciar_carrito(request):
    if 'carrito' in request.session:
        del request.session['carrito']
        messages.success(request, 'Carrito vaciado')
    
    return redirect('carrito')

@login_required
def procesar_compra(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        
        if not carrito:
            messages.error(request, 'El carrito está vacío')
            return redirect('carrito')
        
        # Crear la venta
        cliente = Cliente.objects.get(usuario=request.user)
        total_venta = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
        
        venta = Venta.objects.create(
            cliente=cliente,
            total=total_venta
        )
        
        # Crear detalles de venta
        for producto_id, item in carrito.items():
            producto = Producto.objects.get(id=producto_id)
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item['cantidad'],
                precio=item['precio']
            )
        
        # Vaciar carrito
        del request.session['carrito']
        messages.success(request, f'¡Compra realizada exitosamente! Total: ${total_venta}')
        
        return redirect('index')
    
    return redirect('carrito')

# lala_app/views.py
# lala_app/views.py - Actualizar perfil_cliente
@login_required
def perfil_cliente(request):
    cliente = get_object_or_404(Cliente, usuario=request.user)
    
    # Obtener pedidos del cliente
    ventas = Venta.objects.filter(cliente=cliente).order_by('-fecha')[:10]
       # DEBUG: Mostrar información de cada venta
    print("=" * 50)
    print(f"DEBUG - Pedidos para cliente: {cliente.usuario.username}")
    for venta in ventas:
        print(f"Venta #{venta.id} - Completada: {venta.completada} - Tipo: {type(venta.completada)}")
    print("=" * 50)
    
    
    # Obtener reseñas del cliente
    reseñas_usuario = Resena.objects.filter(cliente=cliente).order_by('-fecha')
    
    if request.method == 'POST':
        # Actualizar información del perfil
        if 'foto_perfil' in request.FILES:
            cliente.foto_perfil = request.FILES['foto_perfil']
            cliente.save()
            messages.success(request, 'Foto de perfil actualizada')
            return redirect('perfil_cliente')
        else:
            # Actualizar datos personales
            cliente.usuario.first_name = request.POST.get('first_name', '')
            cliente.usuario.last_name = request.POST.get('last_name', '')
            cliente.correo = request.POST.get('email', '')
            cliente.telefono = request.POST.get('telefono', '')
            cliente.direccion = request.POST.get('direccion', '')
            
            cliente.usuario.save()
            cliente.save()
            
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('perfil_cliente')
    
    context = {
        'cliente': cliente,
        'ventas': ventas,
        'reseñas_usuario': reseñas_usuario,
    }
    
    return render(request, 'lala_app/perfil_cliente.html', context)
# Vista para agregar productos al carrito (requiere login)
@login_required
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get('cantidad', 1))
        
        # Aquí iría la lógica para agregar al carrito
        # Por ahora solo mostramos un mensaje
        messages.success(request, f'¡{producto.nombre} agregado al carrito!')
        return redirect('productos_lacteos')
    
    return redirect('productos_lacteos')

# ... (el resto de las vistas del admin panel se mantienen igual)

@login_required
@user_passes_test(es_gerente)
def admin_panel(request):
    models_info = {
        'producto': {
            'nombre': 'Productos',
            'count': Producto.objects.count(),
            'icon': '📦',
            'description': 'Gestionar productos del catálogo'
        },
        'cliente': {
            'nombre': 'Clientes',
            'count': Cliente.objects.count(),
            'icon': '👥',
            'description': 'Gestionar información de clientes'
        },
        'empleado': {
            'nombre': 'Empleados',
            'count': Empleado.objects.count(),
            'icon': '👨‍💼',
            'description': 'Gestionar información de empleados'
        },
        'proveedor': {
            'nombre': 'Proveedores',
            'count': Proveedor.objects.count(),
            'icon': '🏢',
            'description': 'Gestionar información de proveedores'
        },
        'resena': {
            'nombre': 'Reseñas',
            'count': Resena.objects.count(),
            'icon': '⭐',
            'description': 'Gestionar reseñas de productos'
        },
        'receta': {
            'nombre': 'Recetas',
            'count': Receta.objects.count(),
            'icon': '📝',
            'description': 'Gestionar recetas'
        },
        'venta': {
            'nombre': 'Ventas',
            'count': Venta.objects.count(),
            'icon': '💰',
            'description': 'Ver historial de ventas'
        }
    }
    return render(request, 'lala_app/admin_panel.html', {'models_info': models_info})

@login_required
@user_passes_test(es_gerente)
def admin_crud_list(request, model_name):
    model_map = {
        'producto': (Producto, 'lala_app/admin_crud/producto_list.html'),
        'cliente': (Cliente, 'lala_app/admin_crud/cliente_list.html'),
        'empleado': (Empleado, 'lala_app/admin_crud/empleado_list.html'),
        'proveedor': (Proveedor, 'lala_app/admin_crud/proveedor_list.html'),
        'resena': (Resena, 'lala_app/admin_crud/resena_list.html'),
        'receta': (Receta, 'lala_app/admin_crud/receta_list.html'),
        'venta': (Venta, 'lala_app/admin_crud/venta_list.html'),
    }
    
    if model_name not in model_map:
        messages.error(request, 'Modelo no encontrado')
        return redirect('admin_panel')
    
    model, template = model_map[model_name]
    objetos = model.objects.all()
    
    context = {
        'model_name': model_name,
        'objetos': objetos,
        'model_display_name': model_name.capitalize()
    }
    
    return render(request, template, context)

@login_required
@user_passes_test(es_gerente)
def admin_crud_create(request, model_name):
    model_form_map = {
        'producto': ProductoForm,
        'empleado': EmpleadoForm,
        'proveedor': ProveedorForm,
        'receta': RecetaForm,
        'resena': ResenaForm,
    }
    
    if model_name not in model_form_map:
        messages.error(request, 'No se puede crear este tipo de objeto')
        return redirect('admin_crud_list', model_name=model_name)
    
    FormClass = model_form_map[model_name]
    
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'{model_name.capitalize()} creado exitosamente')
            return redirect('admin_crud_list', model_name=model_name)
    else:
        form = FormClass()
    
    context = {
        'form': form,
        'model_name': model_name,
        'model_display_name': model_name.capitalize(),
        'action': 'Agregar'
    }
    
    return render(request, 'lala_app/admin_crud/form.html', context)

@login_required
@user_passes_test(es_gerente)
def admin_crud_update(request, model_name, pk):
    model_form_map = {
        'producto': (Producto, ProductoForm),
        'empleado': (Empleado, EmpleadoForm),
        'proveedor': (Proveedor, ProveedorForm),
        'receta': (Receta, RecetaForm),
        'resena': (Resena, ResenaForm),
        'venta': (Venta, VentaAdminForm),
    }
    
    if model_name not in model_form_map:
        messages.error(request, 'No se puede editar este tipo de objeto')
        return redirect('admin_crud_list', model_name=model_name)
    
    ModelClass, FormClass = model_form_map[model_name]
    objeto = get_object_or_404(ModelClass, pk=pk)
    
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=objeto)
        if form.is_valid():
            form.save()
            messages.success(request, f'{model_name.capitalize()} actualizado exitosamente')
            return redirect('admin_crud_list', model_name=model_name)
    else:
        form = FormClass(instance=objeto)
    
    context = {
        'form': form,
        'model_name': model_name,
        'model_display_name': model_name.capitalize(),
        'action': 'Editar',
        'objeto': objeto
    }
    if model_name == 'venta':
        template = 'lala_app/admin_crud/venta_form.html'
    else:
        template = 'lala_app/admin_crud/form.html'
    
    return render(request, 'lala_app/admin_crud/form.html', context)

@login_required
@user_passes_test(es_gerente)
def admin_crud_delete(request, model_name, pk):
    model_map = {
        'producto': Producto,
        'empleado': Empleado,
        'proveedor': Proveedor,
        'receta': Receta,
        'resena': Resena,
        'cliente': Cliente,
    }
    
    if model_name not in model_map:
        messages.error(request, 'No se puede eliminar este tipo de objeto')
        return redirect('admin_crud_list', model_name=model_name)
    
    ModelClass = model_map[model_name]
    objeto = get_object_or_404(ModelClass, pk=pk)
    
    if request.method == 'POST':
        objeto.delete()
        messages.success(request, f'{model_name.capitalize()} eliminado exitosamente')
        return redirect('admin_crud_list', model_name=model_name)
    
    context = {
        'objeto': objeto,
        'model_name': model_name,
        'model_display_name': model_name.capitalize()
    }
    
    return render(request, 'lala_app/admin_crud/confirm_delete.html', context)

# lala_app/views.py
def login_view(request):
    if request.method == 'POST':
        # Permitir login con username o email
        username_or_email = request.POST['username']
        password = request.POST['password']
        
        # Intentar autenticar con username
        user = authenticate(request, username=username_or_email, password=password)
        
        # Si no funciona, intentar con email
        if user is None:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            login(request, user)
            if es_gerente(user):
                return redirect('admin_panel')
            else:
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
        else:
            messages.error(request, 'Usuario/Correo o contraseña incorrectos')
    
    return render(request, 'lala_app/login.html')

def register_view(request):
    if request.method == 'POST':
        form = ClienteRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('index')
    else:
        form = ClienteRegistrationForm()
    
    return render(request, 'lala_app/register.html', {'form': form})

# lala_app/views.py
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Obtener productos relacionados (misma categoría)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria
    ).exclude(id=producto.id)[:4]
    
    # Obtener reseñas del producto
    reseñas = Resena.objects.filter(producto=producto)[:5]
    
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
        'reseñas': reseñas,
    }
    
    return render(request, 'lala_app/detalle_producto.html', context)
@login_required
def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = int(request.POST.get('cantidad', 1))
        
        # Aquí implementaremos la lógica real del carrito
        carrito = request.session.get('carrito', {})
        producto_id_str = str(producto_id)
        
        if producto_id_str in carrito:
            carrito[producto_id_str]['cantidad'] += cantidad
        else:
            carrito[producto_id_str] = {
                'cantidad': cantidad,
                'nombre': producto.nombre,
                'precio': str(producto.precio),
                'foto': producto.foto.url if producto.foto else '',
            }
        
        request.session['carrito'] = carrito
        messages.success(request, f'¡{producto.nombre} agregado al carrito!')
        
        return redirect('detalle_producto', producto_id=producto_id)
    
    return redirect('productos_lacteos')

# lala_app/views.py
# lala_app/views.py - Actualizar la vista agregar_resena
@login_required
def agregar_resena(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cliente = get_object_or_404(Cliente, usuario=request.user)
    
    reseña_existente = Resena.objects.filter(cliente=cliente, producto=producto).first()
    
    if request.method == 'POST':
        form = ResenaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                if reseña_existente:
                    reseña_existente.calificacion = form.cleaned_data['calificacion']
                    reseña_existente.descripcion = form.cleaned_data['descripcion']
                    if 'foto_producto' in request.FILES:
                        reseña_existente.foto_producto = request.FILES['foto_producto']
                    reseña_existente.save()
                    messages.success(request, '¡Reseña actualizada exitosamente!')
                else:
                    reseña = form.save(commit=False)
                    reseña.cliente = cliente
                    reseña.producto = producto
                    reseña.save()
                    messages.success(request, '¡Reseña agregada exitosamente!')
                
                # Redirigir a la página de reseñas
                return redirect('resenas')
                
            except Exception as e:
                messages.error(request, f'Error al guardar la reseña: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        if reseña_existente:
            form = ResenaForm(instance=reseña_existente)
        else:
            form = ResenaForm(initial={'calificacion': 5})
    
    context = {
        'form': form,
        'producto': producto,
        'reseña_existente': reseña_existente,
    }
    
    return render(request, 'lala_app/agregar_resena.html', context)

@login_required
def eliminar_resena(request, reseña_id):
    reseña = get_object_or_404(Resena, id=reseña_id)
    
    if reseña.cliente.usuario != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta reseña')
        return redirect('resenas')
    
    if request.method == 'POST':
        reseña.delete()
        messages.success(request, 'Reseña eliminada exitosamente')
        # Redirigir a reseñas
        return redirect('resenas')
    
    context = {
        'reseña': reseña,
    }
    return render(request, 'lala_app/confirmar_eliminar_resena.html', context)
# lala_app/views.py - Actualizar procesar_compra
@login_required
def procesar_compra(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.error(request, 'El carrito está vacío')
        return redirect('carrito')
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            # Simular procesamiento de pago exitoso
            cliente = Cliente.objects.get(usuario=request.user)
            total_venta = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
            
            # Crear la venta
            venta = Venta.objects.create(
                cliente=cliente,
                total=total_venta
            )
            
            # Crear detalles de venta
            for producto_id, item in carrito.items():
                producto = Producto.objects.get(id=producto_id)
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio=item['precio']
                )
            
            # Vaciar carrito
            del request.session['carrito']
            
            messages.success(request, f'¡Pago procesado exitosamente! Total: ${total_venta:.2f}')
            return redirect('index')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario de pago')
    else:
        form = PagoForm()
    
    total_carrito = sum(float(item['precio']) * item['cantidad'] for item in carrito.values())
    
    context = {
        'form': form,
        'total_carrito': total_carrito,
        'items_carrito': carrito,
    }
    
    return render(request, 'lala_app/procesar_pago.html', context)

# lala_app/views.py - Agregar estas vistas

def detalle_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    
    # Obtener recetas relacionadas (excluyendo la actual)
    recetas_relacionadas = Receta.objects.exclude(id=receta_id)[:3]
    
    context = {
        'receta': receta,
        'recetas_relacionadas': recetas_relacionadas,
    }
    
    return render(request, 'lala_app/detalle_receta.html', context)

def recetas(request):
    recetas_lista = Receta.objects.all().order_by('nombre')
    context = {
        'recetas': recetas_lista,
    }
    return render(request, 'lala_app/recetas.html', context)

@login_required
@user_passes_test(es_gerente)
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    
    context = {
        'venta': venta,
        'detalles': detalles,
        'model_name': 'venta',
        'model_display_name': 'Detalle de Venta',
    }
    
    return render(request, 'lala_app/admin_crud/detalle_venta.html', context)

# lala_app/views.py - Agregar estas vistas
@login_required
def mis_pedidos(request):
    # Obtener el cliente actual
    cliente = get_object_or_404(Cliente, usuario=request.user)
    
    # DEBUG: Imprimir información
    print(f"DEBUG mis_pedidos - Usuario: {request.user.username}")
    print(f"DEBUG mis_pedidos - Cliente ID: {cliente.id}")
    
    # Obtener ventas del cliente
    ventas = Venta.objects.filter(cliente=cliente).order_by('-fecha')
    
    # DEBUG: Imprimir cada venta
    print(f"DEBUG mis_pedidos - Número de ventas: {ventas.count()}")
    for venta in ventas:
        print(f"  Venta #{venta.id}: completada = {venta.completada}")
    
    context = {
        'ventas': ventas,
        'cliente': cliente,
    }
    
    return render(request, 'lala_app/mis_pedidos.html', context)

@login_required
def mis_resenas(request):
    cliente = get_object_or_404(Cliente, usuario=request.user)
    reseñas_usuario = Resena.objects.filter(cliente=cliente).order_by('-fecha')
    
    # Calcular el promedio de calificaciones
    from django.db.models import Avg
    promedio_calificacion = reseñas_usuario.aggregate(
        avg_calificacion=Avg('calificacion')
    )['avg_calificacion']
    
    # Si no hay reseñas, establecer promedio a 0
    if promedio_calificacion is None:
        promedio_calificacion = 0
    
    context = {
        'reseñas_usuario': reseñas_usuario,
        'cliente': cliente,
        'promedio_calificacion': promedio_calificacion,  # Añadir esta variable
    }
    
    return render(request, 'lala_app/mis_resenas.html', context)