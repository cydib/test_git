from django.urls import path
from project_app import views

urlpatterns = [
    path('project_manage/', views.project_manage),
    path('project_manage/create_project/', views.create_project),
    path('project_manage/create_project/save_project/', views.save_project),

]