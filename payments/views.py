from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    """Homepage with payment button"""
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'home.html', context)


def create_payment_intent(request):
    """Create a Payment Intent for $5"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=500,  # $5.00
                currency='usd',
                metadata={
                    'product': 'Coffee',
                    'user_email': data.get('email', 'guest@example.com')
                }
            )
            
            return JsonResponse({
                'clientSecret': intent.client_secret
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle events
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        print(f"🎸 PAYMENT SUCCEEDED!")
        print(f"   Amount: ${payment_intent['amount']/100}")
        print(f"   Email: {payment_intent['metadata']['user_email']}")
        
    elif event['type'] == 'payment_intent.payment_failed':
        print(f"💥 Payment failed!")
    
    return HttpResponse(status=200)