from django.db import models
from entity.models.base_models import User, Role
from django.utils import timezone

class ApplicationStatus(models.TextChoices):
    REJECTED = "REJECTED", "Rejected"
    ACCEPTED = "ACCEPTED", "Accepted"
    PENDING = "PENDING", "Pending"



class JobManager(models.Manager):
    def is_valid(self):
        today = timezone.now().date()
        return self.filter(start_date__lte=today, end_date__gte=today)


class Organisation(models.Model):
    name = models.CharField(max_length=255)
    valuation = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    location = models.TextField()
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': Role.ORG_ADMIN})
    staff_access_code = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class Job(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': Role.USER})
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    max_applicants = models.IntegerField(default=1)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    
    objects = JobManager()

    def __str__(self):
        return self.title


class Application(models.Model):
    applicant = models.ManyToManyField(User, limit_choices_to={'role': Role.USER}, related_name='job_applicants')
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    skill_description = models.TextField()
    resume = models.FileField(upload_to='resumes')
    status = models.CharField(choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
    
    def __str__(self):
        return self.status
    