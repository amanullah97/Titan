from django.urls import path
from .import views

urlpatterns = [
    path('', views.login_user, name = "login"),
    path('logout/', views.logout_user, name = "logout"),
    path('home/', views.home, name = "home"),
    path('add-patient/', views.add_patient, name="add-patient"),
    path('update-patient/<str:pk>/', views.update_patient, name="update-patient"),
    path('delete-patient/<str:pk>/', views.delete_patient, name="delete-patient"),
    path('patient-pool/', views.patient_pool, name="patient-pool"),
    path('stats/', views.stats, name="stats"),
    path('scp-stats/', views.scp_stats, name="scp-stats"),
    path('view-all-notification/', views.view_all_notifications,name='view-all-notification'),
    path('mark-all-notifications-as-read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
    path('mark-notification-as-read/<int:pk>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('api/fetch-patients/', views.fetch_patient_data, name='fetch-patients'),
]