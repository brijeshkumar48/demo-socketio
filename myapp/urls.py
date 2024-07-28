from django.urls import path
from . import views

urlpatterns = [
    path('', views.send_message, name='send_message_page'),
    path('trigger/', views.trigger_node_event),
    path('api/send-message/', views.SendMessageView.as_view(), name='send_message'),
    path('api/file-upload-status/', views.FileUploadStatusView.as_view(), name='file_upload_status'),
]
