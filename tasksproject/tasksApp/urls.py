from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.task_list_view, name="task_list"),
    path('delete/<int:index>', views.delete_task_view, name="delete_task"),
    path('edit/<int:index>', views.edit_task_view, name="edit_task"),
    
]