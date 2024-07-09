from django.shortcuts import render
from rest_framework.views import APIView
from . import serializers, models
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class PostCommentView(APIView):
    # permission_classes
    serializer_class = serializers.CommentSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        comments = models.Comment.objects.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentForSpecificPost(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        post_id = request.query_params.get('post_id')
        if post_id:
            return queryset.filter(post = post_id)
        return queryset

# ak ta post e koto gula comment ase ta daker view
class TotalCommentForSinglePostView(generics.ListAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filter_backends = [CommentForSpecificPost]




