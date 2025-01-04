from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny


from main.forms import TeacherForm, TeacherUserForm
from main.models.users import TEACHER
from main.notification_handler import NotificationManager
from main.models import School, Teacher, AcademicSession, Term, SchoolClass, Student, Subject

from ..serializers import (
    SchoolSerializer,
    TeacherSerializer,
    SchoolClassSerializer,
    AcademicSessionSerializer,
    StudentSerializer,
    TermSerializer,
    SubjectSerializer,
)
from ..permissions import IsAdminOrIsTeacherOrReadOnly, IsAdminOrReadOnly

class StandardResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class SchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SchoolClassViewSet(ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        school = School.get_user_school(user=user)
        return SchoolClass.objects.filter(academic_session__school=school)


class AcademicSessionViewSet(ModelViewSet):
    queryset = AcademicSession.objects.all()
    serializer_class = AcademicSessionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        school = self.request.user  #

        return self.queryset.filter(school=school).select_related(
            'school'
        ).prefetch_related(
            'terms'
        )


    @action(detail=True, methods=['post'])
    def current(self, request):
        user = request.user
        school = user.academic_sessions.first()
        current_session = self.queryset.filter(school=school, is_current=True).first()
        if current_session:
            serializer = self.get_serializer(current_session)
            print(serializer.data)
            return Response(serializer.data)
        return Response({'detail' : 'No current session found'}, status=status.HTTP_404_NOT_FOUND) 
    
    @action(detail=True, methods=['post'])
    def make_session_current(self, request, pk=None):
        academic_session = self.get_object()
        AcademicSession.objects.filter(school=academic_session.school).update(is_current=False)
        academic_session.is_current = True
        academic_session.save()
        return Response({'detail' : 'Academic Session updated as current'})
    
    @action(detail=True, methods=['post'])
    def create_terms_and_classes_manually(self, request, pk=None):
        academic_session = self.get_object()
        academic_session.create_terms()
        academic_session.create_all_classes()
        return Response({'detail' : 'Terms and classes are created successfully'})

class TermViewSet(ModelViewSet):
    serializer_class = TermSerializer
    queryset = Term.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        academic_session_id = self.kwargs.get('academic_session_pk')
        if academic_session_id:
            return self.queryset.filter(academic_session_id=academic_session_id)
        return self.queryset

    # def get_queryset(self, request):
    #   return Term.objects.filter(academic_session_pk=self.kwargs['academic_session_pk'])

    # def get_serializer_context(self):
    #   return {'academic_session_id' : self.kwargs['academic_session_pk']}


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all().select_related('user', 'school')
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['GET', 'PUT'])
    def me(self, request):
        teacher = Teacher.objects.get(user=request.user)

        if request.method == 'GET':
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = TeacherSerializer(teacher, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all().select_related('user', 'school')
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['GET', 'PUT'])
    def me(self, request):
        if request.method == 'GET':
            (teacher, created) = Teacher.objects.get_or_create(
                teacher_id=request.user.id)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = TeacherSerializer(teacher)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def list_teachers(self, request):
        queryset = Teacher.get_school_teachers(request=request)
        search_query = request.GET.get("q", "")
        class_filter = request.GET.get("class", "")

        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query)
                | Q(user__last_name__icontains=search_query)
                | Q(user__email__icontains=search_query)
                | Q(department__icontains=search_query)
                | Q(school_class__name__icontains=search_query)
            )

        if class_filter:
            queryset = queryset.filter(
                subjects__school_class__name=class_filter)

        serializer = TeacherSerializer(queryset.distinct(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def detail_teacher(self, request, pk=None):
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def create_teacher(self, request):
        user_form = TeacherUserForm(request.data)
        teacher_form = TeacherForm(request.data)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.role = TEACHER
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.school = School.get_user_school(request.user)
            teacher.save()
            return Response({"detail": "Teacher created successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"errors": user_form.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def update_teacher(self, request, pk=None):
        teacher = get_object_or_404(Teacher, pk=pk)
        user_form = TeacherUserForm(request.data, instance=teacher.user)
        teacher_form = TeacherForm(request.data, instance=teacher)
        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            teacher_form.save()
            NotificationManager.create_notification(
                user=request.user,
                action='updated',
                object_instance=teacher
            )
            return Response({"detail": "Teacher updated successfully!"})
        return Response({"errors": user_form.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['DELETE'])
    def delete_teacher(self, request, pk=None):
        teacher = get_object_or_404(Teacher, pk=pk)
        teacher.user.delete()
        teacher.delete()
        return Response({"detail": "Teacher deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class  = [StandardResultSetPagination]
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['user__first_name', 'grade']
    search_fields = ['user__first_name', 'user__last_name', 'department', 'student_class__name'] #unique search fields for students

    def get_queryset(self, request):
        qs = Student.get_school_students(request=self.request)
        class_filter = self.request.query_params.get('class', None)
        if class_filter:
            qs = qs.filter(school_class__name__icontain=class_filter)
        return qs.distinct()

    


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrIsTeacherOrReadOnly]
