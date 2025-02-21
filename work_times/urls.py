from django.urls import path
from .views import ProjectListView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, WorkTimeListView, \
    WorkTimeDeleteView, WorkTimeUpdateView, WorkTimeCreateView, CalculateWorkTime

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/create/', ProjectCreateView.as_view(), name='create_project'),
    path('projects/update/<int:pk>/', ProjectUpdateView.as_view(), name='update_project'),
    path('projects/delete/<int:pk>/', ProjectDeleteView.as_view(), name='delete_project'),
    path('', WorkTimeListView.as_view(), name='work_time_list'),
    path('<int:pk>/', WorkTimeListView.as_view(), name='work_time_list_by_project'),
    path('create/', WorkTimeCreateView.as_view(), name='work_time_create'),
    path('update/<int:pk>/', WorkTimeUpdateView.as_view(), name='update_work_time'),
    path('delete/<int:pk>/', WorkTimeDeleteView.as_view(), name='delete_work_time'),
    path('calculate_work_time/<str:date>/', CalculateWorkTime.as_view(), name='calculate_work_time'),
]