# from django.contrib.auth.decorators import user_passes_test
# from django.core.exceptions import PermissionDenied
# from django.contrib.auth.models import Group, Permission, User

# def group_required(group_name):
#     def in_group(user):
#         if user.is_autenticated:
#             if user.groups.filter(name=group_name).exists() or user.is_superuser:
#                 return True
#         raise PermissionDenied
# return user_passes_test(in_group)