from datetime import date

from django.db import models


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    gender = models.CharField(max_length=10, choices=Gender.choices)
    birth_date = models.DateField()

    @property
    def age(self):
        today = date.today()
        years = today.year - self.birth_date.year
        has_had_birthday = (today.month, today.day) >= (
            self.birth_date.month,
            self.birth_date.day,
        )
        return years if has_had_birthday else years - 1

    def __str__(self):
        return f"Patient #{self.pk}"


class Device(models.Model):
    class Brand(models.TextChoices):
        GE = "ge", "GE"
        PHILIPS = "philips", "Philips"
        SIEMENS = "siemens", "Siemens"
        MINDRAY = "mindray", "Mindray"
        DRAGER = "drager", "Drager"

    uid1 = models.CharField(max_length=255)
    uid2 = models.CharField(max_length=255)
    uid3 = models.CharField(max_length=255)
    brand = models.CharField(max_length=20, choices=Brand.choices)
    model = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.get_brand_display()} {self.model} ({self.name})"
