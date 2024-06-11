from django.urls import path
from .views import face_recog_view,face_recog_page

urlpatterns = [
    path('', face_recog_page, name='face_recog_page'),
    path('face_recog/', face_recog_view, name='face_recog'),
]
