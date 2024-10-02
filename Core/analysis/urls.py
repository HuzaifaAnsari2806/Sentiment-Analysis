from django.urls import path

from .views import FileUploadView

urlpatterns=[
    path("file_upload/", FileUploadView.as_view(), name="file-upload")
]