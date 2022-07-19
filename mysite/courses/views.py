from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.mixins import ListModelMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from .permissions import IsTeacherUser
from .serializers import CourseSerializer, TeacherSerializer, ReviewSerializer
from .models import Course, Teacher, Review
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by('-published_at')
    serializer_class = CourseSerializer
    authentication_classes = [SessionAuthentication,
                              TokenAuthentication]
    permission_classes = (IsAdminUser,)

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PUT', 'PATCH']:
            return [IsAdminUser()]
        elif self.request.method in ['PUT', 'PATCH']:
            return [IsTeacherUser()]
        return []

class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    '''
    @action(methods=['GET'], detail=True, url_path=r'courses', url_name='courses')
    def get_queryset(self):
        return Course.objects.filter(pk=self.kwargs["pk"])
    
    def get_serializer_class(self):
        if self.action == "courses":
            return TeacherCoursesSerializer
        else:
            return self.serializer_class
    
    @action(methods=['GET'], detail=True, url_path=r'courses', url_name='courses')
    def TeacherCourses(self, request, pk=None):
        #teacher = self.get_object()
        teacher = self.get_object()
        #queryset = Course.objects.filter(teacher=teacher).order_by('-published_at')
        #serializer_class = CourseSerializer
        serializer = self.get_serializer(teacher)
        return Response(serializer.data)
    '''  
@api_view(['GET'])
def TeacherCoursesViewSet(request, pk):
    user = request.user

    try:
        teacher = Teacher.objects.all().get(pk=pk)
        teacherCourses = Course.objects.filter(teacher=teacher)
    except teacherCourses.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(teacherCourses, many=True)
        return Response(serializer.data)


class ReviewViewSet(GenericViewSet,
                    ListModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Review.objects.filter(user=user)

