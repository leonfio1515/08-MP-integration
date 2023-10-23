from django.shortcuts import render, redirect
import mercadopago
from django.conf import settings
from django.views.generic import TemplateView
from .models import Articulo, Compras, Cliente
from django.http import HttpResponse
#-----------------------------------------------------#

def procesar_pago(art, quantity, price):
    sdk = mercadopago.SDK(settings.PROD_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title":art,
                "quantity":quantity,
                "currency_id":"UYU",
                "unit_price": price
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response['response']
    return preference


class Compra(TemplateView):
    model = Articulo
    template_name = 'compras.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = request.POST
            user_id = request.user

            try:
                if int(form['quantity']) > 0:

                    compra = Compras()
                    art_name = Articulo.objects.get(id=form['article'])
                    client = Cliente.objects.get(user=user_id.id)
                    price = float(form['price']) * float(form['quantity'])
                    quantity = int(form['quantity'])

                    compra.art = art_name
                    compra.client = client
                    compra.quantity = quantity
                    compra.tot_amount = price
                    compra.save()
                    request.session['compra_id'] = compra.id

                    print(art_name.name_art, quantity, price)
                    
                    return redirect('pagar')
                else:
                    print('No se selecciono articulo')
                    return redirect('compras')
            except:
                print('No se selecciono articulo')
                return redirect('compras')

        return redirect('compras')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = Articulo.objects.all()
        context['user'] = self.request.user.username
        return context
    
class Pay(TemplateView):
    template_name = 'pay.html'

    def get(self, request, *args, **kwargs):
        compra_id = request.session.get('compra_id', None)

        if compra_id:
            compra = Compras.objects.get(id=compra_id)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        compra_id = request.session.get('compra_id', None)

        if compra_id:
            self.compra = Compras.objects.get(id = compra_id)
            self.prefecence = procesar_pago(self.compra.name_art, self.compra.quantity, self.compra.price)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'preference'):
            context['preference'] = self.preference['id']
            print(context['preference'])
        print(context['preference'])

        return context


class Test(TemplateView):
    sdk = mercadopago.SDK(settings.PROD_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title":'Articulo',
                "quantity":1,
                "currency_id":"UYU",
                "unit_price": 150
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response['response']
