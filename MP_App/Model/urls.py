from django.urls import path
from .views import *

urlpatterns = [
    # Otras rutas de tu aplicación
    path('procesar_pago/', procesar_pago, name='procesar_pago'),
    path('pagar', Pay.as_view(), name='pagar'),
    path('compras', Compra.as_view(), name='compras'),
    path('test', Test.as_view(), name='test'),
]