from django.shortcuts import render, redirect
from django.contrib import messages
from admins.models import AdminDetails

def home(request):
    return render(request, 'home.html')


def choose_type(request):
    if request.method == 'POST':
        visitor_type = request.POST.get('visitor_type')
        request.session['visitor_type'] = visitor_type
        return redirect('choose_category')
    return render(request, 'choose_type.html')


def choose_category(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        request.session['category'] = category
        if category == 'New Visitor':
            return redirect('visitor_signup')
        elif category == 'Visited Before':
            return redirect('visitor_returning')  
    return render(request, 'choose_category.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            admin = AdminDetails.objects.get(admin_name=username)
        except AdminDetails.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return render(request, 'admin_login.html')

        if admin.check_password(password):
            # Password matched — mark session and update last login
            request.session['admin_id'] = admin.id
            admin.update_last_login()
            return redirect('/admins/dashboard/')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'admin_login.html')



