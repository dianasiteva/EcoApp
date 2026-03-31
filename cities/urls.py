from django.urls import path, include
from cities import views


app_name = 'cities'

urlpatterns = [
    path('', views.CitiesListView.as_view(), name='cities_list'),
    path('create/', views.CitiesCreateView.as_view(), name='cities_create'),
    path('<int:pk>/edit/', views.CitiesUpdateView.as_view(), name='cities_edit'),
    path('<int:pk>/delete/', views.CitiesDeleteView.as_view(), name='cities_delete'),
]
