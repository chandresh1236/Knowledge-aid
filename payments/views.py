import stripe # new

from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import render # new

stripe.api_key = settings.STRIPE_SECRET_KEY # new





class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context
def charge(request): # new
    try:
        if request.method == 'POST':
            charge = stripe.Charge.create(
                amount=500,
                currency='inr',
                description='A Django charge',
                source=request.POST['stripeToken']
                
            )
    except Exception:
        print("gjgig")
    return render(request, 'charge.html')
  
