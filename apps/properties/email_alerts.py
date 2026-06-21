from django.core.mail import send_mail
from django.conf import settings
from .models import SavedSearch, Property
from django.utils import timezone


def check_and_send_alerts():
    saved_searches = SavedSearch.objects.filter(is_active=True)

    for search in saved_searches:
        properties = Property.objects.filter(created_at__gt=search.last_checked)

        if search.city:
            properties = properties.filter(city__icontains=search.city)
        if search.price_min:
            properties = properties.filter(price__gte=search.price_min)
        if search.price_max:
            properties = properties.filter(price__lte=search.price_max)
        if search.bedrooms:
            properties = properties.filter(bedrooms=search.bedrooms)

        if properties.exists():
            send_mail(
                subject=f'Naye Properties Mile - {search.name}',
                message=f'{properties.count()} nayi properties mili hain jo aapki search "{search.name}" se match karti hain.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[search.user.email],
                fail_silently=True,
            )

        search.last_checked = timezone.now()
        search.save()
        
        
        
        