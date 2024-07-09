from django.shortcuts import render
from rest_framework.views import APIView
from posts import serializers
from posts import models
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from posts.permissions import IsAuthorOrReadOnly
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import Account
# Create your views here.

class PostForSpecificUser(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        account_id = request.query_params.get('account_id')
        # print(account_id)
        if account_id:
            return queryset.filter(account = account_id)
        return queryset
    
class PostForUserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    filter_backends = [PostForSpecificUser]

class PostUpload(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PostSerializer

    # def get(self, request, format=None):
    #     posts = models.Post.objects.all()
    #     serializer = serializers.PostSerializer(posts, many=True)
    #     return Response(serializer.data)
    def get_objects(self, user):
        acccount = Account.objects.get(user=user)
        return acccount
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            # print(self.get_objects(request.user))
            serializer.validated_data['account'] = self.get_objects(request.user)
            # print(serializer.validated_data['account'])
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class PostDetail(APIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_objects(self, pk):
        try:
            return models.Post.objects.get(pk=pk)
        except(models.Post.DoesNotExist):
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_objects(pk)
        # serializer = self.serializer_class(post)
        serializer = serializers.PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        post = self.get_objects(pk)
        serializer = self.serializer_class(post, data= request.data)
        if serializer.is_valid():
            if serializer.validated_data['image'] is None:
                serializer.validated_data['image'] = post.image
                
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        post = self.get_objects(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class LikeForSpecificPost(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        post_id = request.query_params.get('post_id')
        if post_id:
            return queryset.filter(post = post_id)
        return queryset

# ak ta post koto gula like ase ta dakar view
class ShowLikeView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Like.objects.all()
    serializer_class = serializers.LikeSerializer
    filter_backends = [LikeForSpecificPost]


#like korar view
class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LikeSerializer

    def get_objects(self, request, post):
        try:
            likes = models.Like.objects.filter(post=post)
        except(models.Like.DoesNotExist):
            likes = None
        
        if likes:
            for like in likes:
                if request.user == like.user: # check kortaci user age ei post e like dece ki na
                    return like.id
            return None
        

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            post = serializer.validated_data['post']
            id = self.get_objects(self.request, post)
            # print(ans)
            if id is None:
                # user er like ta save hocca 
                # print(id)
                serializer.validated_data['user'] = request.user
                serializer.save()
            else:
                # user jodi akta post already like deye thake tobe se jodi second time like dete jai tobe oi like dislike hoi e jabe
                like = models.Like.objects.get(id=id)
                like.delete()
                # print(like.post.account.user.username, like.user.username)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
