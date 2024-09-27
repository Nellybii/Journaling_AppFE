from django.urls import path
from .views import entryView, categoryView, userViews, summaryView

urlpatterns = [
    path('journals/', entryView.JournalEntryListCreateView.as_view(), name='journal-entry-list-create'),
    path('journals/<int:pk>/', entryView.JournalEntryDetailView.as_view(), name='journal-entry-detail'),
    path('category/', categoryView.CategorySerializerCreateView.as_view(), name='category-list-create'),
    path('category/<int:pk>/', categoryView.CategoryDetailView.as_view(), name='category-detail'),  
    path('journals-summary/', summaryView.JournalEntrySummaryView.as_view(), name='journals-summary'),
    path('update/', userViews.UserProfileUpdateView.as_view(), name='user-profile-update'),
]
