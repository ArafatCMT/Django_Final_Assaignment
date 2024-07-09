from rest_framework import serializers
from . import models

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Comment
        fields ='__all__'