from rest_framework import serializers
from auth_token_app.models import User, Story

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
        fields = ['user_id', 'email', 'first_name', 'last_name', 'following', 'articles', 'last_edited']
        
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'