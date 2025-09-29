from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]