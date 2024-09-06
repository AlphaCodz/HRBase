from . import Organisation, Application, OrganisationSerializer
from rest_framework import viewsets


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.select_related("admin")
    serializer_class = OrganisationSerializer