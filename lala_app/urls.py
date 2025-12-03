# lala_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('productos-lacteos/', views.productos_lacteos, name='productos_lacteos'),
    path('productos-no-lacteos/', views.productos_no_lacteos, name='productos_no_lacteos'),
    path('recetas/', views.recetas, name='recetas'),
    path('resenas/', views.resenas, name='resenas'),
    path('carrito/', views.carrito, name='carrito'),
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    # Nueva URL para agregar al carrito
    path('agregar-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
    # URLs para el CRUD del admin panel
    path('admin-panel/<str:model_name>/', views.admin_crud_list, name='admin_crud_list'),
    path('admin-panel/<str:model_name>/agregar/', views.admin_crud_create, name='admin_crud_create'),
    path('admin-panel/<str:model_name>/editar/<int:pk>/', views.admin_crud_update, name='admin_crud_update'),
    path('admin-panel/<str:model_name>/eliminar/<int:pk>/', views.admin_crud_delete, name='admin_crud_delete'),

        # Nuevas URLs para el carrito funcional
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar-carrito/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('procesar-compra/', views.procesar_compra, name='procesar_compra'),

    path('agregar-resena/<int:producto_id>/', views.agregar_resena, name='agregar_resena'),

    path('recetas/', views.recetas, name='recetas'),
    path('receta/<int:receta_id>/', views.detalle_receta, name='detalle_receta'),

    # lala_app/urls.py
    path('detalle-venta/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),

    path('eliminar-resena/<int:reseña_id>/', views.eliminar_resena, name='eliminar_resena'),
    
    # Nueva URL para detalles de venta
    path('detalle-venta/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('mis-resenas/', views.mis_resenas, name='mis_resenas'),
]