from . import (
    # Models
    Organisation, Application, Job, Staff, User,
    
    # Serializers
    OrganisationSerializer, ApplicationSerializer, JobSerializer, StaffSerializer, UserSerializer)

from rest_framework import viewsets, response, status, views
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from organisation.permissions import IsHR
import logging

logger = logging.getLogger(__name__)

class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.select_related("admin")
    serializer_class = OrganisationSerializer
    

class JobViewSet(viewsets.ViewSet):
    def get_queryset(self):
        return Job.objects.select_related("organisation", "created_by")

    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise response.Http404

    def get_serializer(self, *args, **kwargs):
        return JobSerializer(*args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='get_all_jobs', url_name='all_jobs')
    def get_all_jobs(self, request):
        jobs = self.get_queryset()
        job_serializer = self.get_serializer(jobs, many=True)
        return response.Response(job_serializer.data, status=status.HTTP_200_OK)

    # Custom Create Job action
    @action(detail=False, methods=['post'], url_path='create', url_name='create')
    def create_job(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom Update Job action
    @action(detail=True, methods=['put', 'patch'], url_path='update', url_name='update')
    def update_job(self, request, pk=None):
        job = self.get_object(pk)
        serializer = self.get_serializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Custom Delete Job action
    @action(detail=True, methods=['delete'], url_path='delete', url_name='delete')
    def delete_job(self, request, pk=None):
        try:
            job = self.get_object(pk)
        except Job.DoesNotExist:
            logger.error("An Error Occured", exc_info=True)
            raise response.Http404
        
        job.delete()
        return response.Response("Job Deleted Successfully!", status=status.HTTP_204_NO_CONTENT)
    
    
class JoinOrganization(viewsets.ViewSet):
    def get_queryset(self):
        return Staff.objects.select_related("organization").prefetch_related("employee")
    
    def get_object(self, pk):
        try:
            Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            return response.Http404
        
    def get_serializer(self, *args, **kwargs):
        return StaffSerializer(*args, **kwargs)
        
    @action(detail=False, methods=['post'], url_path='join', url_name='join-organisation')
    def join_organisation(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='all_staffs', url_name='all-org-staffs')
    def get_all_my_staffs(self, request, pk=None):        
        if not pk:
            return response.Response("You need to provide an Organisation ID", status=status.HTTP_400_BAD_REQUEST)
        try:
            organisation = Organisation.objects.get(id=pk)
        except Organisation.DoesNotExist:
            logger.error("An Error Occured", exc_info=True)
            return response.Response("Organisation not found", status=status.HTTP_404_NOT_FOUND)
        
        staff_members = Staff.objects.filter(organisation=organisation)
        users = User.objects.filter(organization_employees__in=staff_members)
        
        user_serializers = UserSerializer(users, many=True)
        return response.Response(user_serializers.data, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['post'], url_path='remove_staff', url_name='remove-staff')
    def remove_staff(self, request, pk=None):
        
        """
        This endpoint removes the staff from the Organisation without deleting the staff account.
        """
        if not pk:
            return response.Response("You need to provide an Organisation ID", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            organisation = Organisation.objects.get(id=pk)
        except Organisation.DoesNotExist:
            logger.error("An Error Occured", exc_info=True)
            return response.Response("Organisation not found", status=status.HTTP_404_NOT_FOUND)
        
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return response.Response("You need to provide a Employee ID", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            employee = User.objects.get(id=employee_id)
        except User.DoesNotExist:
            logger.error("An Error Occured", exc_info=True)
            return response.Response("Employee Does Not Exist")
        
        try:
            staff = Staff.objects.get(employee=employee, organisation=organisation)
        except Staff.DoesNotExist:
            logger.error("An Error Occured", exc_info=True)
            return response.Response("Staff not found in this organisation", status=status.HTTP_404_NOT_FOUND)
        
        
        # Remove the staff member from the organisation
        staff.organisation = None
        staff.save()

        # Remove the staff member from the employee ManyToManyField
        staff.employee.remove(User.objects.get(id=employee_id))
        
        return response.Response("Staff removed successfully", status=status.HTTP_200_OK)
        
        
class JobApplication(viewsets.ModelViewSet):
    queryset = Application.objects.select_related("job").prefetch_related("applicant")
    serializer_class = ApplicationSerializer
    permission_classes = [IsHR]