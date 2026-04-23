from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from .forms import UserDetailsForm, VisitorLookupForm
from .models import UserDetails, UserDetailsRecord
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.utils import timezone
from access.models import AccessDetails


def visitor_signup(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            # Store contact number for linking later (e.g., photo capture)
            request.session['contact_no'] = form.cleaned_data['contact_no']
            return redirect('take_photo')  
    else:
        form = UserDetailsForm()
    return render(request, 'visitor_signup.html', {'form': form})

def visitor_returning(request):
    """
    Handles lookup (name + contact), show static details, allow edit,
    and when edit is saved, move previous data to UserDetailsRecord.
    """
    print("Visitor returning view hit:", request.method)
    if request.method == 'POST' and 'lookup' in request.POST:
        # lookup submission
        lookup_form = VisitorLookupForm(request.POST)
        if lookup_form.is_valid():
            name = lookup_form.cleaned_data['name'].strip()
            contact_no = lookup_form.cleaned_data['contact_no'].strip()
            try:
                user = UserDetails.objects.get(contact_no=contact_no)
                # optional: verify name matches (case-insensitive partial)
                if name.lower() not in user.name.lower():
                    # name mismatch; still allow lookup by contact only or show message
                    messages.warning(request, "Name does not fully match the record; fetched by contact number.")
                # store the user in session for later steps, for simplicity store contact
                request.session['contact_no'] = user.contact_no
                # show details page
                return render(request, 'old_visitor_details.html', {'user': user})
            except UserDetails.DoesNotExist:
                messages.error(request, "No record found for that contact number. Please register as a new visitor.")
                # show lookup form again
        # if invalid, fall through to render the form with errors
        return render(request, 'visitor_lookup.html', {'form': lookup_form})

    # Edit flow: open edit form or save edit
    if request.method == 'POST' and 'edit' in request.POST:
        # user clicked "Edit" — redirect to edit form (GET with session contact)
        contact_no = request.session.get('contact_no')
        if not contact_no:
            messages.error(request, "Session expired. Please lookup again.")
            return redirect('visitor_returning')
        user = get_object_or_404(UserDetails, contact_no=contact_no)
        form = UserDetailsForm(instance=user)
        return render(request, 'visitor_edit.html', {'form': form, 'user': user})

    if request.method == 'POST' and 'save_edit' in request.POST:
        contact_no_original = request.session.get('contact_no')
        if not contact_no_original:
            messages.error(request, "Session expired. Please lookup again.")
            return redirect('visitor_returning')

        # Fetch original user and keep a pristine copy
        user = get_object_or_404(UserDetails, contact_no=contact_no_original)
        original_user = UserDetails.objects.get(pk=contact_no_original)  # 🟢 fresh DB copy

        form = UserDetailsForm(request.POST, instance=user)

        if form.is_valid():
            with transaction.atomic():
                # ✅ Archive using original_user (not form-bound instance)
                UserDetailsRecord.objects.create(
                    original_contact_no=original_user.contact_no,
                    name=original_user.name,
                    designation=original_user.designation,
                    company_name=original_user.company_name,
                    company_no=original_user.company_no,
                    address=original_user.address,
                    company_address=original_user.company_address,
                    date_of_birth=original_user.date_of_birth,
                    nid_passport=original_user.nid_passport,
                    image_path=original_user.image.name if original_user.image else None,
                )

                # 🆕 Now save the edited version
                updated_user = form.save(commit=False)
                new_contact_no = form.cleaned_data['contact_no']

                if new_contact_no != user.contact_no:
                    if user.image:
                        updated_user.image = user.image
                    updated_user.pk = new_contact_no
                    updated_user.save()
                    user.delete()
                    request.session['contact_no'] = new_contact_no
                    user = updated_user
                else:
                    updated_user.save()

                messages.success(request, "Information updated and previous record archived.")

            return render(request, 'old_visitor_details.html', {'user': user})
        else:
            return render(request, 'visitor_edit.html', {'form': form, 'user': user})



    # Default: GET -> show lookup form
    lookup_form = VisitorLookupForm()
    return render(request, 'visitor_lookup.html', {'form': lookup_form})

def take_photo(request):
    """
    Renders the webcam capture page.
    """
    return render(request, 'take_photo.html')


def upload_photo(request):
    """
    Receives base64 image from frontend and saves to UserDetails.
    """
    if request.method == 'POST':
           contact_no = request.session.get('contact_no')

    if not contact_no:
        return JsonResponse({'status': 'error', 'message': 'No session found'})

    try:
        visitor = UserDetails.objects.get(contact_no=contact_no)
    except UserDetails.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Visitor not found'})

    image_data = request.POST.get('image')
    if not image_data:
        return JsonResponse({'status': 'error', 'message': 'No image data received'})

    format, imgstr = image_data.split(';base64,')
    ext = format.split('/')[-1]
    file_name = f"{visitor.contact_no}_profile.{ext}"
    visitor.image = ContentFile(base64.b64decode(imgstr), name=file_name)
    visitor.save()

    return JsonResponse({'status': 'success'})

def returning_take_photo(request):
    contact_no = request.session.get('contact_no')
    visitor_type = request.session.get('visitor_type')

    if not contact_no:
        return redirect('old_visitor_details.html')

    visitor = get_object_or_404(UserDetails, contact_no=contact_no)

    # Handle POST (AJAX upload)
    if request.method == 'POST':
        image_data = request.POST.get('image')

        if not image_data:
            return JsonResponse({'status': 'error', 'message': 'No image data received'})

        # Decode and save the image
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        file_name = f"{visitor.contact_no}_{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        visitor_image = ContentFile(base64.b64decode(imgstr), name=file_name)

        # ✅ Save in AccessDetails, NOT in UserDetails
        access_entry = AccessDetails.objects.create(
            visitor=visitor,
            image=visitor_image,
            purpose=visitor_type or "Visitor",
            date=timezone.now().date(),
            time=timezone.now().time()
        )

        # Store for next steps
        request.session['access_id'] = access_entry.id
        request.session['purpose'] = visitor_type
        request.session['host_name'] = None  # Will be set later
        request.session['access_time'] = str(timezone.now())

        return JsonResponse({'status': 'success'})
    # Render shared camera template
    return render(request, 'take_photo.html', {
        'upload_url': 'take-photo'  # dynamic upload endpoint
    })