from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from visitors.models import UserDetails
from .models import AccessDetails, HostList
from .forms import AccessForm

def visitor_access(request):
    contact_no = request.session.get('contact_no')
    visitor_type = request.session.get('visitor_type')  # ✅ comes from core app

    if not contact_no:
        return redirect('visitor_signup')  # fallback if session lost

    visitor = get_object_or_404(UserDetails, contact_no=contact_no)

    if request.method == 'POST':
        form = AccessForm(request.POST)
        if form.is_valid():
            host = form.cleaned_data['host']
            purpose = visitor_type or "Visitor"  # fallback just in case

            today = timezone.now().date()
            count_today = AccessDetails.objects.filter(date=today).count() + 1

            access_record = AccessDetails.objects.create(
                visitor=visitor,
                host=host,
                purpose=purpose,  # ✅ automatically from session
                no_of_visitors_today=count_today,
                time_of_access=timezone.localtime(timezone.now()).time()  # Use local time
            )

            # Store for print preview
            request.session['host_name'] = host.name
            request.session['purpose'] = purpose
            request.session['access_time'] = str(access_record.time_of_access)

            return redirect('print_preview')
    else:
        form = AccessForm()

    return render(request, 'visitor_access.html', {
        'form': form,
        'visitor': visitor,
        'visitor_type': visitor_type
    })
