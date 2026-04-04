from django.urls import path
from events.views import LocationListView, EventListView, EventDetailView, EventCreateView, EventUpdateView, \
    EventDeleteView, LocationDetailView, LocationCreateView, LocationUpdateView, LocationDeleteView, \
    RemoveAssignmentView, event_report, AssignOrganizerView, RemoveOrganizerView

urlpatterns = [
    path('', EventListView.as_view(), name='event_list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/edit/', EventUpdateView.as_view(), name='event_edit'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('locations/', LocationListView.as_view(), name='location_list'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='location_detail'),
    path('locations/create/', LocationCreateView.as_view(), name='location_create'),
    path('locations/<int:pk>/edit/', LocationUpdateView.as_view(), name='location_edit'),
    path('locations/<int:pk>/delete/', LocationDeleteView.as_view(), name='location_delete'),
    path('assignment/<int:per_id>/remove/', RemoveAssignmentView.as_view(), name='remove_assignment'),
    path('events/<int:pk>/report/', event_report, name='event_report'),
    # path('assignment/<int:per_id>/make-organizer/', AssignOrganizerView.as_view(), name='assign_organizer'),
    # path('assignment/<int:per_id>/remove-organizer/', RemoveOrganizerView.as_view(), name='remove_organizer'),
    #
    path('assignment/<int:per_id>/make-organizer/', AssignOrganizerView.as_view(), name='assign_organizer'),
    path('assignment/<int:per_id>/remove-organizer/', RemoveOrganizerView.as_view(), name='remove_organizer'),

]
