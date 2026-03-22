from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Record
from .serializers import RecordSerializer
from .views import _filter_records


class RecordListAPIView(ListAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        queryset = Record.objects.all().order_by('-created_at')
        query = self.request.query_params.get('q', '').strip()
        return _filter_records(queryset, query)


class RecordDetailAPIView(RetrieveAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
