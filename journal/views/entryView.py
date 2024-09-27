from rest_framework import generics, permissions
from ..models import JournalEntry
from ..serializers import JournalEntrySerializer

from rest_framework import generics, permissions
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from ..models import JournalEntry
from ..serializers import JournalEntrySerializer

class JournalEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = JournalEntry.objects.filter(user=self.request.user)

        period_param = self.request.query_params.get('period')
        today = datetime.now().date()

        if period_param == 'daily':
            queryset = queryset.filter(date=today)

        elif period_param == 'weekly':
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            queryset = queryset.filter(date__range=[start_of_week, end_of_week])

        elif period_param == 'monthly':
            start_of_month = today.replace(day=1)
            next_month = start_of_month.replace(month=start_of_month.month + 1, day=1)
            end_of_month = next_month - timedelta(days=1)
            queryset = queryset.filter(date__range=[start_of_month, end_of_month])

        return queryset.order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
class JournalEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)
