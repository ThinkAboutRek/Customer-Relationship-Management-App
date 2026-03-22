import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm, AddRecordForm
from .models import Record

@login_required(redirect_field_name=None)
def home(request):
    query = request.GET.get('q', '').strip()
    records = Record.objects.all()
    if query:
        records = records.filter(
            first_name__icontains=query
        ) | records.filter(
            last_name__icontains=query
        ) | records.filter(
            email__icontains=query
        ) | records.filter(
            company__icontains=query
        )
    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'records': page_obj, 'query': query, 'page_obj': page_obj})

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = SignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
            
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = LoginForm(request=request, data=request.POST or None)
    # 1) If they were redirected here by @login_required, Django appends ?next=…
    if request.method == 'GET' and 'next' in request.GET:
        messages.warning(request, "🔒 Please log in to view that page.")

    # 2) Handle form submission
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, "You have been logged in!")

                # 3) Redirect to `next` if present, else home
                return redirect(request.GET.get('next', 'home'))
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
def customer_record(request, pk):
    # Safely 404 if not found
    record = get_object_or_404(Record, pk=pk)
    return render(request, 'record.html', {'customer_record': record})

@login_required
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Record added!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
            
    return render(request, 'add_record.html', {'form': form})

@login_required
def update_record(request, pk):
    record = get_object_or_404(Record, pk=pk)
    form = AddRecordForm(request.POST or None, instance=record)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
            
    return render(request, 'update_record.html', {'form': form})

@login_required
def export_records_csv(request):
    query = request.GET.get('q', '').strip()
    records = Record.objects.all()
    if query:
        records = records.filter(
            first_name__icontains=query
        ) | records.filter(
            last_name__icontains=query
        ) | records.filter(
            email__icontains=query
        ) | records.filter(
            company__icontains=query
        )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="records.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Company', 'Address', 'City', 'County', 'Postcode', 'Notes', 'Created At'])
    for r in records:
        writer.writerow([r.id, r.first_name, r.last_name, r.email, r.phone, r.company, r.address, r.city, r.county, r.postcode, r.notes, r.created_at.strftime('%Y-%m-%d %H:%M')])
    return response


@login_required
def delete_record(request, pk):
    if request.method == 'POST':
        record = get_object_or_404(Record, pk=pk)
        record.delete()
        messages.success(request, "Record deleted!")
    return redirect('home')