from django.shortcuts import render, redirect
import mercadopago
from django.conf import settings
from django.views.generic import TemplateView

#-----------------------------------------------------#

def procesar_pago(request):
    sdk = mercadopago.SDK(settings.PROD_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title":"Producto",
                "quantity":1,
                "currency_id":"UYU",
                "unit_price": 500.00
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response['response']['id']
    print(preference)
    return redirect(preference['init_point'])


class Pay(TemplateView):
    template_name = 'pay.html'

    sdk = mercadopago.SDK(settings.PROD_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title":"Producto",
                "quantity":1,
                "currency_id":"UYU",
                "unit_price": 500.00
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response['response']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['preference'] = self.preference['id']
        print(context['preference'])
        return context
