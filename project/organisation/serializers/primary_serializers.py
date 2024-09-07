from rest_framework import serializers
from . import Application, Organisation, Job, User
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class OrganisationSerializer(serializers.ModelSerializer):
    staff_access_code = serializers.CharField(read_only=True)
    class Meta:
        model = Organisation
        fields = "__all__"
        

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['created_by', "organisation", "title", "description", "max_applicants", "start_date", "end_date", "applicant_count"]

    def validate_organisation(self, value):
        try:
            # Check if the Organisation exists
            Organisation.objects.get(id=value.id)
        except Organisation.DoesNotExist:
            raise serializers.ValidationError(f"This Organisation '{value}' does not exist.")
            logger.error(f"An Error Occured", exc_info=True)
        return value
    
    def validate_end_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Invalid date: Please ensure the job's closing date is not set in the past.")
        return value
    
    def validate(self, attrs):
        max_applicants = attrs.get("max_applicants")
        applicant_count = attrs.get("applicant_count")
        if max_applicants == applicant_count:
            raise serializers.ValidationError("Sorry, Unfortunately we are not accepting any more applications")
        return attrs
    
    
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["id", "applicant", "job", "skill_description", "resume", "status"]
        
    def validate_applicant(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("This User Does Not Exist")
            logger.error(f"An Error Occured", exc_info=True)
        return value
    
    def create(self, validated_data):
        instance = Application(**validated_data)
        
        # Increase Job Applicant Count
        job = instance.job
        job.applicant_count += 1
        job.save()
        
        instance.save()
        return instance