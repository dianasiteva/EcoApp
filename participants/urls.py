from django.urls import path

from .views import (
    ParticipantListView,
    ParticipantDetailView,
    ParticipantUpdateView,
    assign_role, ParticipantCreateView, ParticipantDeleteView,
)

urlpatterns = [
    path('', ParticipantListView.as_view(), name='participant_list'),
    path('<int:pk>/', ParticipantDetailView.as_view(), name='participant_detail'),
    path('create/', ParticipantCreateView.as_view(), name='participant_create'),
    path('<int:pk>/edit/', ParticipantUpdateView.as_view(), name='participant_edit'),
     path('<int:pk>/delete/', ParticipantDeleteView.as_view(), name='participant_delete'),
    path('assign/<int:event_id>/', assign_role, name='assign_role'),

]