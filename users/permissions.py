from django.contrib.auth.models import Group, Permission
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class MyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request):
        return Response({'status': 'request was permitted'})


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
