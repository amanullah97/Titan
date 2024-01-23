from django.contrib import admin
from .models import Provider, Insurance, Patient, InsuranceType, Notification, PatientActivity
# Register your models here.
admin.site.register(Provider)
admin.site.register(Insurance)
admin.site.register(InsuranceType)
admin.site.register(Patient)
admin.site.register(Notification)
admin.site.register(PatientActivity)
