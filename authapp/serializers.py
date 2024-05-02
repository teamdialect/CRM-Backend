from rest_framework import serializers
from authapp.models import CustomUser,Lead,Task


class UserSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = CustomUser
        fields = [ 'id','username', 'email', 'password', 'profile_picture', 'name', 'mobile_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class LeadSerializer(serializers.ModelSerializer):
    assigned_user = serializers.SlugRelatedField(queryset=CustomUser.objects.all(),slug_field='username')

    class Meta:
        model = Lead
        fields = "__all__"

class TaskSerializer(serializers.ModelSerializer):
    assigned_user = serializers.SlugRelatedField(queryset=CustomUser.objects.all(),slug_field='username')

    class Meta:
        model = Task
        fields = [ 'id', 'name', 'description', 'from_date', 'to_date', 'priority', 'checklists','assigned_user']