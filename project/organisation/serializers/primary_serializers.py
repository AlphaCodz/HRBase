from rest_framework import serializers
from . import Application, Organisation


class OrganisationSerializer(serializers.ModelSerializer):
    staff_access_code = serializers.CharField(read_only=True)
    class Meta:
        model = Organisation
        fields = "__all__"
        