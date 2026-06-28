from django.contrib.auth.models import Group, Permission
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from groups import moderator_group

can_change_course_permission = Permission.objects.get(codename='Can change Курс')
can_add_course_permission = Permission.objects.get(codename='Can add Курс')
can_view_course_permission = Permission.objects.get(codename='Can view Курс')
can_delete_course_permission = Permission.objects.get(codename='Can delete Курс')
can_change_lesson_permission = Permission.objects.get(codename='Can change Урок')
can_add_lesson_permission = Permission.objects.get(codename='Can add Урок')
can_view_lesson_permission = Permission.objects.get(codename='Can view Урок')
can_delete_lesson_permission = Permission.objects.get(codename='Can delete Урок')


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class MyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        return Response({'status': 'request was permitted'})


def has_permission(self, request, view):
    if request.user.groups.filter(name='Moderators').exists():
        moderator_group.permissions.add(can_change_course_permission, can_view_course_permission,
                                        can_change_lesson_permission, can_view_lesson_permission)


def get_permissions(self):
    if self.action == 'create':
        self.permission_classes = [can_add_course_permission, can_add_lesson_permission]
    elif self.action == 'list':
        self.permission_classes = [can_delete_course_permission, can_delete_lesson_permission]
    return [permission() for permission in self.permission_classes]


class ChangeLessonListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, can_change_lesson_permission]


class ViewLessonListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, can_view_lesson_permission]


class GroupCanEditOrReadOnly(permissions.BasePermission):
    message = "Модераторам разрешены только редактирование и просмотр."

    def has_permission(self, request, view) -> bool:

        if not request.user.is_authenticated:
            return False

        group = Group.objects.get(name='Moderators')
        return group in request.user.groups.all()

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if obj.owner == request.user:
                return True
            return False
