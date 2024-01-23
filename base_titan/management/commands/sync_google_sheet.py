from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from base_titan.models import Patient, Provider, Insurance, InsuranceType
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import re


class Command(BaseCommand):
    help = 'Sync data from Google Sheet'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)

    def handle(self, *args, **options):
        user_id = options['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with ID {user_id} does not exist"))
            return

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/g_key.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1CQj4WEwiH1cJdigaJnYcCZbbnK3W6oRoAKhY921DUwg").sheet1
        data = sheet.get_all_records()
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"

        for row in data:
            # InsuranceType.objects.create(ins_type = row["Insurance Type"])
            gender = row["Gender"]

            # Check if the gender value is one of the valid choices
            if gender not in [choice[0] for choice in Patient.GENDER_CHOICES]:
                gender = None

            dob_str = row["DOB"]
            try:
                dob = datetime.strptime(dob_str, "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                # Handle invalid date format here
                print(f"Invalid date format for DOB: {dob_str}")
                dob = None

            provider_name = row["Provider"]
            try:
                provider = Provider.objects.get(name=provider_name)
            except Provider.DoesNotExist:
                provider = None

            insurance_name = row["Insurance"]
            try:
                insurance = Insurance.objects.get(name=insurance_name)
            except Insurance.DoesNotExist:
                insurance = None

            insurance_type = row["TOI"]
            try:
                _insurance_type = InsuranceType.objects.get(ins_type =  insurance_type)
            except InsuranceType.DoesNotExist:
                _insurance_type = None

            status = row["Status"]
            if status not in [choice[0] for choice in Patient.status_choices]:
                status = None

            _assistant = row["Assistant"]
            try:
                assistant = User.objects.get(username = _assistant)
            except User.DoesNotExist:
                assistant = None

            hb1ac = row["HBA1C"]
            if hb1ac not in [choice[0] for choice in Patient.HB_CHOICES]:
                hb1ac = None

            enrolled_in_pcm_ccm = row["Enrolled In CCM_PCM"]
            if enrolled_in_pcm_ccm not in [choice[0] for choice in Patient.CCM_PCM_CHOICES]:
                enrolled_in_pcm_ccm = None

            enrolled_in_bhi = row["Enrolled In BHI"]
            if enrolled_in_bhi not in [choice[0] for choice in Patient.BHI_CHOICES]:
                enrolled_in_bhi = None

            enrolled_in_rpm = row["Enrolled In RPM"]
            if enrolled_in_rpm not in [choice[0] for choice in Patient.RPM_CHOICES]:
                enrolled_in_rpm = None

            suboxone = row["Suboxone"]
            if suboxone not in [choice[0] for choice in Patient.CHOICES]:
                suboxone = None

            medical_marijuana = row["Medical Marijuana"]
            if medical_marijuana not in [choice[0] for choice in Patient.CHOICES]:
                medical_marijuana = None

            transitional_care_visit = row["Transitional care visit"]
            if transitional_care_visit not in [choice[0] for choice in Patient.TRANS_CHOICES]:
                transitional_care_visit = None

            other_med = row["Other Controlled Medication"]
            if other_med not in [choice[0] for choice in Patient.CHOICES]:
                other_med = None

            try:
               last_appointment = row["Last Appointemnt"]
               if not re.match(date_pattern, last_appointment):
                   last_appointment = None
            except (ValueError):
               last_appointment = None

            try:
                registration_date = row["Date Of Registration"]
                if not re.match(date_pattern, registration_date):
                    registration_date = None
            except (ValueError):
                registration_date = None

            try:
                bw_done = row["BW Done"]
                if not re.match(date_pattern, bw_done):
                    bw_done = None
            except (ValueError):
                bw_done = None

            try:
                hb1ac_date = row["HBA1C Reading Date"]
                if not re.match(date_pattern, hb1ac_date):
                    hb1ac_date = None
            except (ValueError):
                hb1ac_date = None

            try:
                fobt_date = row["FOBT Date"]
                if not re.match(date_pattern, fobt_date):
                    fobt_date = None
            except (ValueError):
                fobt_date = None

            try:
                colonoscopy_date = row["Colonoscopy"]
                if not re.match(date_pattern, colonoscopy_date):
                    colonoscopy_date = None
            except (ValueError):
                colonoscopy_date = None

            try:
                pap_smear_date = row["Pap Smear"]
                if not re.match(date_pattern, pap_smear_date):
                    pap_smear_date = None
            except (ValueError):
                pap_smear_date = None

            try:
                mammogram_date = row["Mammogram Date"]
                if not re.match(date_pattern, mammogram_date):
                    mammogram_date = None
            except (ValueError):
                mammogram_date = None

            try:
                last_uds_date = row["Last UDS Date"]
                if not re.match(date_pattern, last_uds_date):
                    last_uds_date = None
            except (ValueError):
                last_uds_date = None

            try:
                med_reconcile_date = row["Med Reconcilation Date"]
                if not re.match(date_pattern, med_reconcile_date):
                    med_reconcile_date = None
            except (ValueError):
                med_reconcile_date = None

            try:
                last_hospital_vist = row["Last ER Visit"]
                if not re.match(date_pattern, last_hospital_vist):
                    last_hospital_vist = None
            except (ValueError):
                last_hospital_vist = None

            try:
                annual_wellness_vist = row["Annual Wellness Visit Date"]
                if not re.match(date_pattern, annual_wellness_vist):
                    annual_wellness_vist = None
            except (ValueError):
                annual_wellness_vist = None

            try:
                follow_up = row["Follow Up Appointment"]
                if not re.match(date_pattern, follow_up):
                    follow_up = None
            except (ValueError):
                follow_up = None

            try:
                reading_date = row["Reading Date"]
                if not re.match(date_pattern, reading_date):
                    reading_date = None
            except (ValueError):
                reading_date = None

            try:
                cologuard_date = row["Cologuard"]
                if not re.match(date_pattern, cologuard_date):
                    cologuard_date = None
            except (ValueError):
                cologuard_date = None

            try:
                last_anthropometric_date = row["Last Anthropometric Date"]
                if not re.match(date_pattern, last_anthropometric_date):
                    last_anthropometric_date = None
            except (ValueError):
                last_anthropometric_date = None

            Patient.objects.create(
                name = row["Patients Names"],
                gender = gender,
                assistant = assistant,
                operator = user,
                provider = provider,
                date_of_birth = dob,
                insurance = insurance,
                insurance_type = _insurance_type,
                status = status,
                hb1ac = hb1ac,
                enrolledin_PCM_CCM = enrolled_in_pcm_ccm,
                enrolledin_BHI = enrolled_in_bhi,
                enrolledin_RPM = enrolled_in_rpm,
                suboxone = suboxone,
                medical_marijuana = medical_marijuana,
                other_controlled_med = other_med,
                transitional_care_vist = transitional_care_visit,
                last_appointment = last_appointment,
                registration_date = registration_date,
                referred_by = row["Referred By"],
                follow_up = follow_up,
                last_anthropometric_date = last_anthropometric_date,
                last_bmi = row["Last BMI"],
                last_bp_reading = row["Blood Pressure Reading"],
                reading_date = reading_date,
                bw_done = bw_done,
                hb1ac_date = hb1ac_date,
                fobt_date = fobt_date,
                colonoscopy_date = colonoscopy_date,
                cologuard_date = cologuard_date,
                pap_smear_date = pap_smear_date,
                mammogram_date = mammogram_date,
                chronic_condition = row["Chronic Condition"],
                last_uds_date = last_uds_date,
                last_hospital_vist = last_hospital_vist,
                annual_wellness_vist = annual_wellness_vist,
                med_reconcile_date = med_reconcile_date,
                comments = row["Comments"]
            )







            #
            #     # Create the Patient object, ensuring that the related objects are valid
            #     if dob and provider and insurance:
            #         Patient.objects.create(
            #             name=row["Name"],
            #             date_of_birth=dob,  # Use the converted date
            #             gender=gender,
            #             provider=provider,
            #             insurance=insurance
            #             # Add other fields as needed
            #         )
            #     else:
            #         # Handle cases where the date format, provider, or insurance is invalid
            #         # You can log an error message or skip the row as needed
            #         print(f"Invalid date format, provider, or insurance for row: {row}")
            #
            # else:
            #     # Handle invalid gender values here, such as logging or skipping the row
            #     print(f"Invalid gender value: {gender}")

        self.stdout.write(self.style.SUCCESS("Data sync completed"))



# from django.core.management.base import BaseCommand
# from base_titan.models import Patient, Provider, Insurance
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
#
#
# class Command(BaseCommand):
#     help = 'Sync data from Google Sheet'
#
#     def handle(self, *args, **options):
#         scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#         creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/g_key.json", scope)
#         print(creds)
#         client = gspread.authorize(creds)
#         sheet = client.open_by_key("1CQj4WEwiH1cJdigaJnYcCZbbnK3W6oRoAKhY921DUwg").sheet1
#         # worksheet = sheet.get_worksheet(0)
#         data = sheet.get_all_records()
#
#         for row in data:
#             # provider_name = row['Provider']  # Assuming 'provider' column in the sheet
#             # provider, created = Provider.objects.get_or_create(name=provider_name)
#
#             Insurance.objects.create(
#                 name = row["Inusrance"],
#                 titan_user = ""
#                 # Add other fields as needed
#             )