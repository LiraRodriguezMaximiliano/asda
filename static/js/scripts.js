// static/lala_app/js/scripts.js

// Funcionalidades generales del sitio LALA
document.addEventListener('DOMContentLoaded', function() {
    // =============================================
    // 1. MANEJO DE MENSAJES DEL SISTEMA
    // =============================================
    
    // Cerrar mensajes manualmente
    const closeButtons = document.querySelectorAll('.close-message');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.alert').style.display = 'none';
        });
    });

    // Auto-ocultar mensajes después de 5 segundos
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert.style.display !== 'none') {
                alert.style.animation = 'fadeOut 0.5s ease-out';
                setTimeout(() => {
                    alert.style.display = 'none';
                }, 500);
            }
        });
    }, 5000);

    // =============================================
    // 2. FUNCIONALIDADES DE PRODUCTOS
    // =============================================
    
    // Validación de cantidad en formularios
    const quantityInputs = document.querySelectorAll('input[type="number"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 1) this.value = 1;
            if (this.value > 100) this.value = 100; // Aumentamos el límite
        });
        
        input.addEventListener('input', function() {
            if (this.value < 0) this.value = 1;
        });
    });

    // Agregar al carrito con validación
    const addToCartForms = document.querySelectorAll('form[action*="agregar-carrito"]');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const cantidadInput = this.querySelector('input[name="cantidad"]');
            if (cantidadInput && (cantidadInput.value < 1 || cantidadInput.value > 100)) {
                e.preventDefault();
                showMessage('error', 'La cantidad debe ser entre 1 y 100');
                return;
            }
            
            // Mostrar mensaje de carga
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.textContent;
                submitBtn.textContent = 'Agregando...';
                submitBtn.disabled = true;
                
                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                }, 2000);
            }
        });
    });

    // =============================================
    // 3. FUNCIONALIDADES DEL CARRITO
    // =============================================
    
    // Cantidad en carrito
    const quantityButtons = document.querySelectorAll('.quantity-btn');
    quantityButtons.forEach(button => {
        button.addEventListener('click', function() {
            const isPlus = this.classList.contains('plus');
            const quantityElement = this.parentElement.querySelector('.quantity');
            let quantity = parseInt(quantityElement.textContent);
            
            if (isPlus) {
                quantity++;
            } else if (quantity > 1) {
                quantity--;
            }
            
            quantityElement.textContent = quantity;
            actualizarTotalCarrito();
        });
    });

    // Eliminar items del carrito
    const removeButtons = document.querySelectorAll('.btn-remove');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const item = this.closest('.cart-item');
            item.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                item.remove();
                actualizarTotalCarrito();
                showMessage('success', 'Producto eliminado del carrito');
            }, 300);
        });
    });

    // =============================================
    // 4. FUNCIONALIDADES DEL PERFIL
    // =============================================
    
    // Navegación del perfil
    const navLinks = document.querySelectorAll('.nav-link');
    const profileSections = document.querySelectorAll('.profile-section');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            
            // Actualizar navegación activa
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Mostrar sección correspondiente
            profileSections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetId) {
                    section.classList.add('active');
                }
            });
        });
    });

    // =============================================
    // 5. FUNCIONALIDADES DE RESEÑAS
    // =============================================
    
    // Modal de reseñas
    const reviewModal = document.getElementById('reviewModal');
    const btnAddReview = document.getElementById('btnAddReview');
    const closeModal = document.querySelector('.close');
    const starSelects = document.querySelectorAll('.star-select');

    if (btnAddReview) {
        btnAddReview.addEventListener('click', function() {
            if (reviewModal) {
                reviewModal.style.display = 'block';
                cargarProductosParaResena();
            }
        });
    }

    if (closeModal) {
        closeModal.addEventListener('click', function() {
            if (reviewModal) {
                reviewModal.style.display = 'none';
            }
        });
    }

    // Selección de estrellas
    starSelects.forEach(star => {
        star.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            const ratingInput = document.getElementById('rating');
            if (ratingInput) {
                ratingInput.value = value;
            }
            
            // Actualizar visualización de estrellas
            starSelects.forEach(s => {
                if (s.getAttribute('data-value') <= value) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
        });
    });

    // =============================================
    // 6. FUNCIONALIDADES DEL ADMIN PANEL
    // =============================================
    
    // Confirmación para eliminaciones
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar este elemento?')) {
                e.preventDefault();
            }
        });
    });

    // Búsqueda en tablas del admin
    const searchInputs = document.querySelectorAll('.table-search');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const table = this.closest('.table-container').querySelector('tbody');
            const rows = table.querySelectorAll('tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // =============================================
    // 7. FUNCIONALIDADES GENERALES DE LA PÁGINA
    // =============================================
    
    // Smooth scroll para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Lazy loading para imágenes
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Animación de contadores en estadísticas
    const statCounters = document.querySelectorAll('.stat-info h3');
    statCounters.forEach(counter => {
        const target = parseInt(counter.textContent);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const updateCounter = () => {
            current += step;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        // Iniciar cuando el elemento sea visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(counter);
    });

    // =============================================
    // 8. MANEJO DE FORMULARIOS
    // =============================================
    
    // Validación de formularios
    const forms = document.querySelectorAll('form:not([action*="agregar-carrito"])');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showMessage('error', 'Por favor completa todos los campos requeridos');
            }
        });
    });

    // Limpieza de errores en inputs
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.style.borderColor = '';
        });
    });
});

// =============================================
// FUNCIONES GLOBALES
// =============================================

// Función para mostrar mensajes
function showMessage(type, message) {
    const messagesContainer = document.querySelector('.messages-container') || createMessagesContainer();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type}`;
    messageDiv.textContent = message;
    
    const closeBtn = document.createElement('button');
    closeBtn.className = 'close-message';
    closeBtn.innerHTML = '&times;';
    closeBtn.addEventListener('click', () => {
        messageDiv.style.animation = 'fadeOut 0.5s ease-out';
        setTimeout(() => messageDiv.remove(), 500);
    });
    
    messageDiv.appendChild(closeBtn);
    messagesContainer.appendChild(messageDiv);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.style.animation = 'fadeOut 0.5s ease-out';
            setTimeout(() => messageDiv.remove(), 500);
        }
    }, 5000);
}

// Crear contenedor de mensajes si no existe
function createMessagesContainer() {
    const container = document.createElement('div');
    container.className = 'messages-container';
    document.body.appendChild(container);
    return container;
}

// Actualizar total del carrito
function actualizarTotalCarrito() {
    const cartItems = document.querySelectorAll('.cart-item');
    let subtotal = 0;
    
    cartItems.forEach(item => {
        const price = parseFloat(item.querySelector('.item-price').textContent.replace('$', ''));
        const quantity = parseInt(item.querySelector('.quantity').textContent);
        const total = price * quantity;
        
        item.querySelector('.item-total').textContent = `$${total.toFixed(2)}`;
        subtotal += total;
    });
    
    const subtotalElement = document.querySelector('.summary-row:first-child span:last-child');
    const totalElement = document.querySelector('.summary-row.total span:last-child');
    
    if (subtotalElement) subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
    if (totalElement) totalElement.textContent = `$${subtotal.toFixed(2)}`;
}

// Cargar productos para reseñas (simulación)
function cargarProductosParaResena() {
    const productSelect = document.getElementById('product');
    if (productSelect && productSelect.children.length <= 1) {
        // Simular carga de productos
        const products = [
            { id: 1, name: 'Leche LALA Entera 1L' },
            { id: 2, name: 'Yogurt LALA Fresa' },
            { id: 3, name: 'Queso LALA Manchego' },
            { id: 4, name: 'Crema LALA' }
        ];
        
        products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.id;
            option.textContent = product.name;
            productSelect.appendChild(option);
        });
    }
}

// Función para formatear precios
function formatPrice(price) {
    return new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN'
    }).format(price);
}

// Función para validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Función para validar teléfono (México)
function isValidPhone(phone) {
    const phoneRegex = /^[0-9]{10}$/;
    return phoneRegex.test(phone.replace(/\D/g, ''));
}

// Cerrar modal al hacer clic fuera
window.addEventListener('click', function(event) {
    const modal = document.getElementById('reviewModal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

// Manejar tecla ESC para cerrar modales
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.style.display = 'none';
        });
    }
});

// =============================================
// ANIMACIONES CSS DINÁMICAS
// =============================================

// Agregar estilos CSS dinámicamente para animaciones
const dynamicStyles = `
@keyframes fadeOut {
    from { opacity: 1; transform: translateY(0); }
    to { opacity: 0; transform: translateY(-20px); }
}

@keyframes slideOut {
    from { opacity: 1; transform: translateX(0); }
    to { opacity: 0; transform: translateX(100%); }
}

.lazy {
    opacity: 0;
    transition: opacity 0.3s;
}

.lazy.loaded {
    opacity: 1;
}
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = dynamicStyles;
document.head.appendChild(styleSheet);

// =============================================
// INICIALIZACIÓN DE COMPONENTES
// =============================================

// Inicializar tooltips
function initTooltips() {
    const elementsWithTooltip = document.querySelectorAll('[data-tooltip]');
    elementsWithTooltip.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - tooltip.offsetHeight - 5) + 'px';
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTooltips);
} else {
    initTooltips();
}

// Exportar funciones para uso global (si es necesario)
window.LALA = {
    showMessage,
    formatPrice,
    isValidEmail,
    isValidPhone
};

// En static/lala_app/js/scripts.js - Agregar esta función
function setupCartQuantityButtons() {
    // Botones de cantidad en el carrito
    const quantityButtons = document.querySelectorAll('.quantity-btn');
    quantityButtons.forEach(button => {
        button.addEventListener('click', function() {
            const isPlus = this.classList.contains('plus');
            const quantityElement = this.parentElement.querySelector('.quantity');
            let quantity = parseInt(quantityElement.textContent);
            
            if (isPlus) {
                quantity++;
            } else if (quantity > 1) {
                quantity--;
            }
            
            quantityElement.textContent = quantity;
            updateCartItem(this.closest('.cart-item'), quantity);
        });
    });
}

function updateCartItem(itemElement, newQuantity) {
    const itemId = itemElement.id.replace('item-', '');
    const price = parseFloat(itemElement.querySelector('.item-price').textContent.replace('$', ''));
    const totalElement = itemElement.querySelector('.item-total');
    const newTotal = price * newQuantity;
    
    totalElement.textContent = `$${newTotal.toFixed(2)}`;
    updateCartTotal();
    
    // Enviar actualización al servidor
    updateCartOnServer(itemId, newQuantity);
}

function updateCartTotal() {
    const cartItems = document.querySelectorAll('.cart-item');
    let subtotal = 0;
    
    cartItems.forEach(item => {
        const total = parseFloat(item.querySelector('.item-total').textContent.replace('$', ''));
        subtotal += total;
    });
    
    const subtotalElement = document.querySelector('.summary-row:first-child span:last-child');
    const totalElement = document.querySelector('.summary-row.total span:last-child');
    
    if (subtotalElement) subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
    if (totalElement) totalElement.textContent = `$${subtotal.toFixed(2)}`;
}

function updateCartOnServer(itemId, quantity) {
    // Esta función enviaría la actualización al servidor
    // Por ahora solo actualizamos la interfaz
    console.log(`Actualizando item ${itemId} a cantidad ${quantity}`);
}