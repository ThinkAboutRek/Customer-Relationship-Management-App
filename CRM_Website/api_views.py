from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Record
from .serializers import RecordSerializer


class RecordListAPIView(ListAPIView):
    serializer_class = RecordSerializer

    def get_queryset(self):
        queryset = Record.objects.all().order_by('-created_at')
        query = self.request.query_params.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                first_name__icontains=query
            ) | queryset.filter(
                last_name__icontains=query
            ) | queryset.filter(
                email__icontains=query
            ) | queryset.filter(
                company__icontains=query
            )
        return queryset


class RecordDetailAPIView(RetrieveAPIView):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
