from rest_framework import generics, permissions
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from ..models import JournalEntry
from ..serializers import JournalEntrySerializer

class JournalEntrySummaryView(generics.ListAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = JournalEntry.objects.filter(user=self.request.user)
        period_param = self.request.query_params.get('period')
        start_date_param = self.request.query_params.get('start_date')
        end_date_param = self.request.query_params.get('end_date')

        if period_param == 'daily' and start_date_param:
            try:
                start_date = datetime.strptime(start_date_param, '%Y-%m-%d').date()
                queryset = queryset.filter(date=start_date)
            except ValueError:
                queryset = JournalEntry.objects.none()

        elif period_param == 'weekly' and start_date_param and end_date_param:
            try:
                start_date = datetime.strptime(start_date_param, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_param, '%Y-%m-%d').date()
                queryset = queryset.filter(date__range=[start_date, end_date])
            except ValueError:
                queryset = JournalEntry.objects.none()

        elif period_param == 'monthly' and start_date_param:
            try:
                start_date = datetime.strptime(start_date_param, '%Y-%m').date()
                start_of_month = start_date.replace(day=1)
                next_month = start_of_month.replace(month=start_of_month.month + 1, day=1)
                end_of_month = next_month - timedelta(days=1)
                queryset = queryset.filter(date__range=[start_of_month, end_of_month])
            except ValueError:
                queryset = JournalEntry.objects.none()

        return queryset.order_by('-date')
