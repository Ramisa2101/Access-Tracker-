from django.shortcuts import render, redirect
from visitors.models import UserDetails
from access.models import AccessDetails
from django.utils import timezone

def print_preview(request):
    contact_no = request.session.get('contact_no')
    visitor_type = request.session.get('visitor_type')  # from core step
    host_name = request.session.get('host_name')
    purpose = request.session.get('purpose')
    access_time = request.session.get('access_time')

    if not contact_no:
        return redirect('core:home')  # fallback if session lost

    # Get visitor info from DB
    try:
        visitor = UserDetails.objects.get(contact_no=contact_no)
    except UserDetails.DoesNotExist:
        return redirect('core:home')

    context = {
        'visitor': visitor,
        'visitor_type': visitor_type,
        'host_name': host_name,
        'purpose': purpose,
        'date': timezone.now().strftime('%Y-%m-%d'),
        'time': timezone.now().strftime('%H:%M:%S'),
    }

    return render(request, 'print_preview.html', context)
