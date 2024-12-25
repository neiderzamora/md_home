from rest_framework import permissions

class CanViewPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.can_view_patient')

class CanEditPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.can_edit_patient')

class CanViewDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.can_view_doctor')

class CanEditDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('users.can_edit_doctor')