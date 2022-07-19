from rest_framework import serializers

from .models import Course, Teacher, Review
from accounts.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'created', 'updated', 'title', 'description', 'teacher', 'price', 'published_at', 'get_avg_score']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = "__all__"
        #fields = ['id', 'user', 'created', 'updated']

        
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Review
        fields = "__all__"
