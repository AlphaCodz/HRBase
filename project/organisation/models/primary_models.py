from django.db import models
from entity.models.base_models import User, Role
from django.utils import timezone
import random, string

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
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': "USER"})
    staff_access_code = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['location']),
            models.Index(fields=['longitude', 'latitude']),
            models.Index(fields=['admin']),
            models.Index(fields=['staff_access_code']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]
        
        constraints = [
            models.UniqueConstraint(fields=['staff_access_code'], name='unique_staff_code'),
        ]
    
    def save(self, *args, **kwargs):
        if not self.staff_access_code:
            self.staff_access_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=3))
        super(Organisation, self).save(*args, **kwargs)


class Job(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': "USER"})
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    max_applicants = models.IntegerField(default=1)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    applicant_count = models.IntegerField(default=0)
    
    objects = JobManager()

    def __str__(self):
        return self.title
    
    class Meta:
        indexes = [
            models.Index(fields=['created_by']),
            models.Index(fields=['organisation']),
            models.Index(fields=['title']),
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
            models.Index(fields=['applicant_count']),
            models.Index(fields=['created_by', 'organisation']),  # Composite index
            models.Index(fields=['start_date', 'end_date']),  # Composite index
        ]


class Application(models.Model):
    STATUS = (
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("PENDING", "Pending")
    )
    applicant = models.ManyToManyField(User, limit_choices_to={'role': "USER"}, related_name='job_applicants')
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    skill_description = models.TextField()
    resume = models.FileField(upload_to='resumes')
    status = models.CharField(choices=STATUS, default="PENDING")

    def __str__(self):
        return self.status
    
    class Meta:
        indexes = [ 
            models.Index(fields=['job']),       
            models.Index(fields=['status']), # Composite index
        ]

    def save(self, *args, **kwargs):
        if self.job:
            self.job.applicant_count += 1
        super().save(*args, **kwargs)
            

class Staff(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, null=True)
    employee = models.ManyToManyField(User, limit_choices_to={'role': "USER"}, related_name='organization_employees')
    org_access_code = models.CharField(max_length=5, unique=True, null=True)
    
    def __str__(self):
        return self.organisation.name
    
    class Meta:
            indexes = [
            models.Index(fields=['organisation']),  # Index for querying by organisation
            models.Index(fields=['org_access_code']),  # Index for querying by org_access_code
            models.Index(fields=['organisation', 'org_access_code']),  # Composite index for organisation and org_access_code
        ]
    
    def save(self, *args, **kwargs):
        if not self.org_access_code:
            self.org_access_code = "".join(random.choices(string.digits + string.ascii_uppercase, k=5))
        # Call the parent class's save method first to save the instance

        super().save(*args, **kwargs)
        
        # Update employee roles if this is a new Staff instance
        if self.pk:  # Check if the instance has been saved
            employees = self.employee.all()
            for employee in employees:
                if employee.role != "ORG_STAFF":  # Check if the role needs to be updated
                    try:
                        with transaction.atomic():
                            employee.role = "ORG_STAFF"
                            employee.save()
                            # Optionally log this update
                            # logger.debug(f"Updated role for employee {employee.id} to ORG_STAFF")
                    except Exception as e:
                        # Optionally log the exception
                        # logger.error(f"Error updating role for employee {employee.id}: {e}", exc_info=True)
                        pass