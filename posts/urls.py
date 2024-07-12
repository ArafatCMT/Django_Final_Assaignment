from rest_framework.routers import DefaultRouter
from django.urls import path, include
from posts import views

router = DefaultRouter()
router.register('new', views.PostUploadViewSet)

urlpatterns = [
    path('upload/', views.PostUpload.as_view(), name='postlist'),
    path('user/', views.PostForUserView.as_view()),
    path('detail/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('total/likes/', views.ShowLikeView.as_view()),
    path('like/', views.LikeView.as_view()),
    path('',include(router.urls))
]