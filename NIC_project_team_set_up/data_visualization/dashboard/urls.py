from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-states/', views.get_states, name='get_states'),
    path('get-kpis/', views.get_kpis, name='get_kpis'),
    path('process_form/', views.process_form, name='process_form'),    
]
