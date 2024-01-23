# models.py
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class Provider(models.Model):
    titan_user = models.ForeignKey(User,  on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name


class Insurance(models.Model):
    titan_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name


class InsuranceType(models.Model):
    titan_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ins_type = models.CharField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.ins_type


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        null=True, blank=True
    )
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    assistant = models.ForeignKey(User, related_name="assistant", blank=True,null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=False, blank=False)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    patient_appointment = models.DateField(null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    insurance = models.ForeignKey(Insurance, on_delete = models.SET_NULL, null=True, blank=True)
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.SET_NULL, null=True, blank=True)
    status_choices = [
        ('Another PCP', 'Another PCP'),
        ('Inactive Insurance', 'Inactive Insurance'),
        ('Patient with Follow Up appointment', 'Patient with Follow Up appointment'),
        ('Blank Patient', 'Blank Patient'),
        ('N/A', 'N/A'),
        ('Referred', 'Referred'),
        ('Clear', 'Clear'),
        ('Deceased', 'Deceased'),
        ('Unreachable', 'Unreachable'),
        ('Terminated', 'Terminated'),

    ]
    status = models.CharField(null=True, blank=True, choices=status_choices)
    referred_by = models.CharField(null=True, blank=True)
    last_appointment = models.DateField(null=True, blank=True)
    follow_up = models.DateField(null=True, blank=True)
    last_anthropometric_date = models.DateField(null=True, blank=True)

    last_bmi = models.CharField(null=True, blank=True)
    last_bp_reading = models.CharField(null=True, blank=True)
    reading_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    bw_done = models.DateField(null=True, blank=True)
    hb1ac_date = models.DateField(null=True, blank=True)
    HB_CHOICES = [
        ('4-6', '4-6'),
        ('6-8', '6-8'),
        ('8-10', '8-10'),
        ('10-12', '10-12'),
        ('12-14', '12-14'),
        ('>14', '>14'),
    ]
    hb1ac = models.CharField(
        choices=HB_CHOICES,
        null=True, blank=True
    )
    fobt_date = models.DateField(null=True, blank=True)
    colonoscopy_date = models.DateField(null=True, blank=True)
    cologuard_date = models.DateField(null=True, blank=True)
    pap_smear_date = models.DateField(null=True, blank=True)
    mammogram_date = models.DateField(null=True, blank=True)

    chronic_condition = models.CharField(null=True, blank=True)
    CCM_PCM_CHOICES = [
        ('Enrolled In PCM', 'Enrolled In PCM'),
        ('Enrolled In CCM', 'Enrolled In CCM'),
        ('Not Interested', 'Not Interested'),
        ('left the program', 'left the program'),
        ('Not Eligible', 'Not Eligible'),
    ]
    enrolledin_PCM_CCM = models.CharField(
        choices=CCM_PCM_CHOICES,
        null=True, blank=True
    )
    BHI_CHOICES = [
        ('Enrolled In BHI', 'Enrolled In BHI'),
        ('Not Eligible', 'Not Eligible'),
        ('left the program', 'left the program'),
        ('Not Interested', 'Not Interested'),
    ]
    enrolledin_BHI = models.CharField(
        choices=BHI_CHOICES,
        null=True, blank=True
    )
    RPM_CHOICES = [
        ('BP Set', 'BP Set'),
        ('Glucometer', 'Glucometer'),
        ('IScale', 'IScale'),
        ('Weight', 'Weight'),
        ('Not Interested', 'Not Interested'),
        ('left the program', 'left the program'),
        ('Not Eligible', 'Not Eligible'),
    ]
    enrolledin_RPM = models.CharField(
        choices=RPM_CHOICES,
        null=True, blank=True
    )

    CHOICES = [
        ('YES', 'YES'),
        ('NO', 'NO'),
    ]
    suboxone = models.CharField(
        choices=CHOICES,
        null=True, blank=True
    )
    medical_marijuana = models.CharField(
        choices=CHOICES,
        null=True, blank=True
    )
    other_controlled_med = models.CharField(
        choices=CHOICES,
        null=True, blank=True
    )
    last_uds_date = models.DateField(null=True, blank=True)

    last_hospital_vist = models.DateField(null=True, blank=True)
    annual_wellness_vist = models.DateField(null=True, blank=True)
    TRANS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
    ]
    transitional_care_vist = models.CharField(
        choices = TRANS_CHOICES,
        null=True, blank=True
    )
    acp = models.DateField(null=True, blank=True)
    med_reconcile_date = models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-updated", "-created"]
        unique_together = ['name', 'date_of_birth']

    @property
    def age(self):
        if not self.date_of_birth:
            return 0
        today = datetime.today()
        age = today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age

    def __str__(self):
        return self.name


class PatientActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    field_edited = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} edited {self.field_edited} for {self.patient.name}"