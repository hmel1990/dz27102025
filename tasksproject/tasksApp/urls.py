from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    
    path('', views.task_list_view, name="task_list"),
    path('delete/<int:index>', views.delete_task_view, name="delete_task"),
    path('edit/<int:index>', views.edit_task_view, name="edit_task"),
    path('result/', views.result, name="result_middleware"),
    path("normalize/", views.normalize_user_data, name="normalize_user_data"),
    path("check-agent/", views.user_agent_check_view, name="check_agent"),
    path("mobile-page/", lambda r: HttpResponse("Мобильная версия сайта"), name="mobile_page"),
    path("templatelist/", views.template_tasklist, name="template_list"),
    path("groupedtemplatelist/", views.grouped_template_tasklist, name="grouped_template_list"),
]