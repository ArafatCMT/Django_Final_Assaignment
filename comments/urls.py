from django.urls import path, include
from comments import views


urlpatterns = [
   path('list/', views.PostCommentView.as_view(), name='comment_list'),
   path('specific/post/', views.TotalCommentForSinglePostView.as_view(), name='comment_list_per_post'),
]