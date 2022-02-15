from django.urls import path
from . import views

app_name = 'calcluator'

urlpatterns = [

    path('', views.main_page, name='main_page'),
    path('set_demensions/', views.set_demensions, name='set_demensions'),
    path('result', views.result, name='result'),

]