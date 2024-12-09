from rest_framework import serializers
from .models import Survey, MediaItem, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'phone']

class MediaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaItem
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    media_items = MediaItemSerializer(many=True, read_only=True)
    investigator = UserProfileSerializer(read_only=True)

    class Meta:
        model = Survey
        fields = [
            'id', 'name', 'longitude', 'latitude', 
            'start_date', 'end_date', 'investigator', 
            'created_at', 'updated_at', 'media_items'
        ]
        read_only_fields = ['investigator', 'created_at', 'updated_at']