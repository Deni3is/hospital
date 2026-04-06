from datetime import date

from django.core.management.base import BaseCommand

from registry.models import Device, Patient


class Command(BaseCommand):
    help = "Create demo patients and devices so the dashboard has sample data."

    def handle(self, *args, **options):
        patient_birth_dates = [
            date(1980, 1, 15),
            date(1984, 3, 22),
            date(1988, 5, 10),
            date(1991, 7, 4),
            date(1993, 9, 18),
            date(1996, 11, 2),
            date(1999, 2, 27),
            date(2001, 6, 14),
            date(2004, 8, 30),
            date(2007, 12, 9),
        ]
        patient_genders = [
            Patient.Gender.MALE,
            Patient.Gender.FEMALE,
            Patient.Gender.OTHER,
            Patient.Gender.FEMALE,
            Patient.Gender.MALE,
            Patient.Gender.FEMALE,
            Patient.Gender.MALE,
            Patient.Gender.OTHER,
            Patient.Gender.FEMALE,
            Patient.Gender.MALE,
        ]

        device_specs = [
            (Device.Brand.GE, "Vivid S70", "Cardiology Room 1"),
            (Device.Brand.PHILIPS, "Affiniti 70", "Cardiology Room 2"),
            (Device.Brand.SIEMENS, "Acuson Redwood", "Ultrasound Room 1"),
            (Device.Brand.MINDRAY, "DC-80", "Ultrasound Room 2"),
            (Device.Brand.DRAGER, "Savina 300", "ICU Station 1"),
            (Device.Brand.GE, "Venue Go", "Emergency Room"),
            (Device.Brand.PHILIPS, "Epiq CVx", "Echo Lab"),
            (Device.Brand.SIEMENS, "Acuson Sequoia", "Diagnostics Room"),
            (Device.Brand.MINDRAY, "BeneVision N19", "ICU Station 2"),
            (Device.Brand.DRAGER, "Infinity Delta", "Monitoring Post"),
        ]

        patients_created = 0
        for index, birth_date in enumerate(patient_birth_dates, start=1):
            _, created = Patient.objects.get_or_create(
                birth_date=birth_date,
                defaults={"gender": patient_genders[index - 1]},
            )
            if created:
                patients_created += 1

        devices_created = 0
        for index, (brand, model, name) in enumerate(device_specs, start=1):
            _, created = Device.objects.get_or_create(
                uid1=f"UID1-{index:03d}",
                uid2=f"UID2-{index:03d}",
                uid3=f"UID3-{index:03d}",
                defaults={
                    "brand": brand,
                    "model": model,
                    "name": name,
                },
            )
            if created:
                devices_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo data ready. Patients created: {patients_created}, devices created: {devices_created}."
            )
        )
        self.stdout.write(
            f"Totals in database: patients={Patient.objects.count()}, devices={Device.objects.count()}."
        )
