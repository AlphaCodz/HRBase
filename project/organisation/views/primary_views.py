from . import Organisation, Application, Job, OrganisationSerializer, ApplicationSerializer, JobSerializer
from rest_framework import viewsets, response, status
from rest_framework.decorators import action


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