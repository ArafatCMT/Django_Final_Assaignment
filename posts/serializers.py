from rest_framework import serializers
from posts import models

class PostSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Post
        fields = '__all__'

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     request = self.context.get('request')
    #     if instance.image and request:
    #         representation['image_url'] = request.build_absolute_uri(instance.image.url)
    #     return representation


class LikeSerializer(serializers.ModelSerializer):
    # post = serializers.StringRelatedField(many=False)
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Like
        fields = '__all__'