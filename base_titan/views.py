from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Patient, Provider, Insurance, PatientActivity
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import PatientForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from notifications.signals import notify
from notifications.models import Notification
from django.core import serializers
from django.http import JsonResponse
from datetime import date, datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse


def login_user(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Invalid Attempt!")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or Password does not exist!")

    context = {"page": page}
    return render(request, 'base/login.html', context=context)


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required(login_url = "login" )
def home(request):
    notifications = Notification.objects.filter(recipient=request.user)
    patients_data = serializers.serialize("json", Patient.objects.all())
    patients = Patient.objects.all()[:5]
    context = {
        "patients": patients,
        "notifications": notifications,
        "patients_data": patients_data

    }
    return render(request, 'base/home.html', context)


@login_required(login_url = "login" )
def stats(request):
    statuses = ['Active', 'Inactive', 'Deceased', 'Terminated', 'Unreachable', 'N/A', 'Blank-Patient']
    status_counts = {status: 0 for status in statuses}

    six_months = datetime.now() - timedelta(days=180)
    patients = Patient.objects.all()

    for patient in patients:
        if patient.last_appointment and patient.last_appointment >= six_months.date() and patient.status not in status_counts:
            status_counts['Active'] += 1
        elif patient.status not in status_counts:
            status_counts['Inactive'] += 1
        else:
            if patient.status in status_counts:
                status_counts[patient.status] += 1

    labels = list(status_counts.keys())
    data = list(status_counts.values())

    context = {"labels": labels, "data": data, "data_labels" : zip(data, labels), "patients" : patients}
    return render(request, "base/stats.html", context)


@login_required(login_url = "login" )
def scp_stats(request):
    statuses = []
    patients = Patient.objects.all()
    for patient in patients:
        if patient.status != None:
            statuses.append(patient.status)

    status_counts = {status: 0 for status in statuses}

    for patient in patients:
        if patient.status in status_counts:
            status_counts[patient.status] += 1

    labels = list(status_counts.keys())
    data = list(status_counts.values())

    context = {"labels": labels, "data": data, "data_labels" : zip(data, labels), "patients" : patients}
    return render(request, "base/scp_stats.html", context)


@csrf_exempt
def fetch_patient_data(request):
    if request.method == 'POST':
        data = request.POST  # Extract data from the request

        # Process and store the data in your Django app as needed
        # Example: Save to database
        # ...

        return JsonResponse({'message': 'Data received and processed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@login_required(login_url="login")
def add_patient(request):

    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.operator = request.user
            patient.save()
            if patient.patient_appointment and patient.assistant:
                notify.send(
                    sender=request.user,
                    recipient = patient.assistant,
                    timestamp=timezone.now(),
                    verb=f"Added new appointment for Patient: {patient.name}",
                    description=f"Added new appointment for Patient: {patient.name}",

                )

            if patient.assistant:
                notify.send(
                    sender=request.user,
                    timestamp = timezone.now(),
                    recipient=patient.assistant,
                    verb=f"Added new Patient: {patient.name}",
                    description=f"Added new Patient: {patient.name}",
                )
            messages.success(request, f"Patient: {patient.name} has been added successfully!")
            return redirect("patient-pool")
        else:
            print(form.errors)

    else:
        form = PatientForm()

    context = {"form": form}
    return render(request, "base/patient_form.html", context)


@login_required(login_url='login')
def update_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    form = PatientForm(instance=patient)
    edited_fields = []

    if request.method == "POST":
        original_patient = Patient.objects.get(id=pk)
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            # Create a copy of the original patient instance
            # original_patient = deepcopy(patient)

            # Update and save the patient record
            updated_patient = form.save(commit=False)
            updated_patient.operator = request.user
            updated_patient.save()

            # Compare the updated instance with the original instance

            for field in Patient._meta.fields:  # Iterate through the model's fields
                field_name = field.name


                if getattr(original_patient, field_name) != getattr(updated_patient, field_name):
                    if field_name == "updated" or field_name == "operator":
                        continue
                    edited_fields.append(field_name)

            # Create a PatientActivity record for each edited field
            for field_name in edited_fields:
                activity = PatientActivity(
                    user=request.user,
                    patient=updated_patient,
                    field_edited=field_name.capitalize().replace("_", " ")
                )
                activity.save()

            if updated_patient.patient_appointment and updated_patient.assistant:
                notify.send(
                    sender=request.user,
                    recipient=updated_patient.assistant,
                    verb=f'added a new appointment for patient {updated_patient.name}',
                )
            messages.success(request, f"Patient: {patient.name} has been updated successfully!")
            return redirect("patient-pool")

    else:
        form = PatientForm(instance=patient)

    context = {"form": form, "patient": patient}
    return render(request, 'base/edit_form.html', context)


@login_required(login_url = "login")
def delete_patient(request, pk):
    patient = Patient.objects.get(id = pk)
    assistant = patient.assistant
    patient_name = patient.name
    if request.method == "POST":
        patient.delete()
        notify.send(
            sender=request.user,
            recipient = assistant,
            verb = f'Deleted Patient: {patient_name}'
        )
        return redirect("patient-pool")
    context = {"obj": patient}
    return render(request, 'base/delete.html', context)


@login_required(login_url = "login")
def view_all_notifications(request):
    all_notifications = request.user.notifications.all()
    return render(request, 'base/all_notifications.html', {'notifications': all_notifications})


@login_required(login_url="login")
def mark_notification_as_read(request, pk):
    notification = Notification.objects.get(id=pk)

    if notification.unread:
        notification.mark_as_read()

    return redirect("home")


@login_required(login_url="login")
def mark_all_notifications_as_read(request):
    notifications = request.user.notifications.unread()
    notifications.mark_all_as_read()

    return redirect("home")


@login_required(login_url="login")
def patient_pool(request):
    search_option = request.GET.get('search_option')
    search_query = request.GET.get('search_query')

    if search_option == 'patient':
        patients = Patient.objects.filter(
            Q(name__icontains=search_query) |
            Q(date_of_birth__icontains=search_query) |
            (Q(name__istartswith=search_query[:2]) & Q(name__iendswith=search_query[-2:]))
        )
    elif search_option == 'insurance':
        patients = Patient.objects.filter(insurance__name__icontains=search_query)
    else:
        patients = Patient.objects.all()

    # Pagination
    page = request.GET.get('page', 1)
    if search_option == 'insurance':
        per_page = patients.count()  # Show all results for insurance search
    else:
        per_page = request.GET.get('per_page', 10)  # Default per page

    if not patients.exists() or per_page == 0:
        # Handle the case where there are no results or per_page is 0
        patients_page = patients  # Return all patients
    else:
        paginator = Paginator(patients, per_page)
        patients_page = paginator.get_page(page)

    context = {"patients": patients_page, "search_option": search_option, "search_query": search_query}
    return render(request, 'base/patient_pool.html', context)



