from django.urls import path
from .views import procesar_pago, Pay

urlpatterns = [
    # Otras rutas de tu aplicación
    path('procesar_pago/', procesar_pago, name='procesar_pago'),
    path('pagar/', Pay.as_view(), name='pagar'),
]