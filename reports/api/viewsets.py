from rest_framework.viewsets import ModelViewSet

from reports.api.serializers import ReportSerializer
from reports.models import Report


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
