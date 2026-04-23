from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from admins.models import AdminDetails
from django.db.models import Q 
from access.models import AccessDetails, HostList
from visitors.models import UserDetails,UserDetailsRecord

def admin_dashboard(request):
    """Shows a basic dashboard page after login."""
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.error(request, "Please log in first.")
        return redirect('login')

    try:
        admin = AdminDetails.objects.get(id=admin_id)
    except AdminDetails.DoesNotExist:
        messages.error(request, "Invalid session. Please log in again.")
        return redirect('login')

    context = {
        'admin': admin
    }
    admin.refresh_from_db()
    return render(request, 'dashboard.html', context)

def admin_logout(request):
    if 'admin_id' in request.session:
        del request.session['admin_id']
    messages.info(request, "You have been logged out.")
    return redirect('/login/')

def access_list(request):
    """
    Displays access records and allows searching and deletion.
    """
    query = request.GET.get('q', '')  # Get search term from the query string
    if query:
        access_details = AccessDetails.objects.filter(
            Q(visitor__name__icontains=query) |  # Search by visitor name
            Q(purpose__icontains=query)  # Search by purpose
        ).select_related('host')
    else:
        access_details = AccessDetails.objects.all().select_related('host')  # Show all if no search term

    if request.method == 'POST' and 'delete' in request.POST:
        access_id = request.POST.get('delete')
        try:
            access_record = AccessDetails.objects.get(id=access_id)
            access_record.delete()
            messages.success(request, f"Access record for {access_record.visitor.name} deleted successfully.")
        except AccessDetails.DoesNotExist:
            messages.error(request, "Access record not found.")

    return render(request, 'access_list.html', {'access_details': access_details, 'query': query})

def user_list(request):
    query = request.GET.get('q', '')  # Get search term from the query string
    if query:
        # Filter UserDetails based on the query
        user_details = UserDetails.objects.filter(
            Q(name__icontains=query) |  # Search by name
            Q(contact_no__icontains=query) |  # Search by contact number
            Q(company_name__icontains=query)  # Search by company name
        )
    else:
        user_details = UserDetails.objects.all()  # Show all if no search term

    if request.method == 'POST' and 'delete' in request.POST:
        user_id = request.POST.get('delete')
        try:
            user_record = UserDetails.objects.get(id=user_id)
            user_record.delete()
            messages.success(request, f"User {user_record.name} deleted successfully.")
        except UserDetails.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, 'user_list.html', {'user_details': user_details, 'query': query})

def archive_list(request):
    query = request.GET.get('q', '')
    if query:
        archives = UserDetailsRecord.objects.filter(
            Q(name__icontains=query) |
            Q(original_contact_no__icontains=query) |
            Q(company_name__icontains=query)
        )
    else:
        archives = UserDetailsRecord.objects.all()

    if request.method == 'POST' and 'delete' in request.POST:
        record_id = request.POST.get('delete')
        try:
            record = UserDetailsRecord.objects.get(id=record_id)
            record.delete()
            messages.success(request, f"Archived record for {record.name} deleted successfully.")
        except UserDetailsRecord.DoesNotExist:
            messages.error(request, "Archive record not found.")

    return render(request, 'archive_list.html', {'archives': archives, 'query': query})

def host_list(request):
    query = request.GET.get('q', '')
    if query:
        hosts = HostList.objects.filter(
            Q(name__icontains=query) |
            Q(designation__icontains=query) |
            Q(contact_no__icontains=query)
        )
    else:
        hosts = HostList.objects.all()

    # ✅ Add new host
    if request.method == 'POST' and 'add_host' in request.POST:
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        contact_no = request.POST.get('contact_no')

        if HostList.objects.filter(contact_no=contact_no).exists():
            messages.warning(request, f"Host with contact {contact_no} already exists.")
        else:
            count = HostList.objects.count() + 1
            HostList.objects.create(
                name=name,
                designation=designation,
                contact_no=contact_no,
                no_of_hosts=count
            )
            messages.success(request, f"Host {name} added successfully.")
        return redirect('admins:host_list')

    # ✅ Edit host
    if request.method == 'POST' and 'edit_host' in request.POST:
        host_id = request.POST.get('edit_host')
        host = get_object_or_404(HostList, id=host_id)
        host.name = request.POST.get('name')
        host.designation = request.POST.get('designation')
        host.contact_no = request.POST.get('contact_no')
        host.save()
        messages.success(request, f"Host {host.name} updated successfully.")
        return redirect('admins:host_list')

    # ✅ Delete host
    if request.method == 'POST' and 'delete_host' in request.POST:
        host_id = request.POST.get('delete_host')
        try:
            host = HostList.objects.get(id=host_id)
            host.delete()
            messages.success(request, f"Host {host.name} deleted successfully.")
        except HostList.DoesNotExist:
            messages.error(request, "Host not found.")
        return redirect('admins:host_list')

    return render(request, 'host_list.html', {'hosts': hosts, 'query': query})
