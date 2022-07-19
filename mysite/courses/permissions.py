from re import T
from urllib import request
from .models import Course, Teacher, Review
from rest_framework.permissions import BasePermission


class IsTeacherUser(BasePermission):
    """
    Allows access only to Teacher users.
    """

    def has_permission(self, request, view):
        return bool(request.user and Teacher.objects.filter(user=request.user).exists())
