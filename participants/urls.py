from django.urls import path
from participants import views

urlpatterns = [
    # Participant URLs
    path('', views.participant_list, name='participant_list'),
    path('<int:pk>/', views.participant_detail, name='participant_detail'),
    path('register/', views.participant_create, name='participant_create'),
    path('<int:pk>/edit/', views.participant_edit, name='participant_edit'),
    path('<int:pk>/delete/', views.participant_delete, name='participant_delete'),
    path('assign/<int:event_id>/', views.assign_role, name='assign_role'),

]