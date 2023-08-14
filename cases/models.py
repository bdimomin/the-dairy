from django.db import models
from users.models import CustomUser
from django.core.validators import FileExtensionValidator

class BulkUpload(models.Model):
    file = models.FileField(upload_to="files/",blank=True,null=True,validators=[FileExtensionValidator(['csv', 'xls', 'xlsx'])])
    date = models.DateTimeField(auto_now_add=True)


class CaseType(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    case_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.case_type}"

class Court(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    court = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.court}"

class PoliceStation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    station = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.station}"

class Client(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    chamber_file_number = models.PositiveIntegerField(blank=True, null=True)
    Representative = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    additional_mobile = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    short_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Case(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    case_type = models.ForeignKey(CaseType, on_delete=models.CASCADE, blank=True, null=True)
    court = models.ForeignKey(Court, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    first_party = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, related_name='first_party_cases')
    appointed_by = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, related_name='appointed_cases')
    law_and_section = models.TextField()
    case_no = models.PositiveIntegerField()
    police_station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE, blank=True, null=True)
    fixed_for = models.TextField(blank=True, null=True)
    second_party = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True, related_name='second_party_cases')
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    STATUS_CHOICES = (
        ('Running', 'Running'),
        ('Decided', 'Decided'),
        ('Abandoned', 'Abandoned'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Running')
    updated = models.BooleanField(default=False)

    def __str__(self):
        return f"Case {self.case_no}"
