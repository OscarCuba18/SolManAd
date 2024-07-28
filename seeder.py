import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolManAd.settings')

import django
django.setup()

from ticket.models import State
from django.contrib.auth.models import Group, Permission, User

states = ["Pendiente", "En curso", "Terminado"]
user_roles = ["Solicitante", "EncargadoMantenimiento", "PersonalMantenimiento"]
solicitante_permissions = ['add_maintenancerequest', 'view_maintenancerequest', 'add_comment', 'view_comment']
encargado_permissions = ['view_maintenancerequest', 'add_assignament', 'change_assignament', 'view_comment']
personal_permissions = ['view_maintenancerequest', 'view_comment', 'add_comment']

def create_user_roles_and_assign_permissions():
    for user_role in user_roles:
        group, created = Group.objects.get_or_create(name=user_role)
        if user_role == 'Solicitante':
            for solicitante_permission in solicitante_permissions:
                permission = Permission.objects.get(codename=solicitante_permission)
                group.permissions.add(permission)
            print(f"Roles de usuarios creados: {user_role} y permisos asignados: {solicitante_permissions}")
        if user_role == 'EncargadoMantenimiento':
            for encargado_permission in encargado_permissions:
                permission = Permission.objects.get(codename=encargado_permission)
                group.permissions.add(permission)
            print(f"Roles de usuarios creados: {user_role} y permisos asignados: {encargado_permissions}")
        if user_role == 'PersonalMantenimiento':
            for personal_permission in personal_permissions:
                permission = Permission.objects.get(codename=personal_permission)
                group.permissions.add(permission)
            print(f"Roles de usuarios creados: {user_role} y permisos asignados: {personal_permissions}")
    print("Todo salio bien")

def add_states():
    for state in states:
        State.objects.create(name=state)
    print(f"Estados creados: {states}")

def create_users_and_assign_groups():
    # Datos de los usuarios a crear
    user_data = [
        {'username': 'solicitante', 'password': '1234', 'group': 'Solicitante'},
        {'username': 'encargado', 'password': '1234', 'group': 'EncargadoMantenimiento'},
        {'username': 'personal', 'password': '1234', 'group': 'PersonalMantenimiento'}
    ]

    for data in user_data:
        # Crear usuario
        user, created = User.objects.get_or_create(username=data['username'])
        if created:
            user.set_password(data['password'])
            user.save()
            print(f"Usuario creado: {data['username']}")

        # Asignar usuario al grupo
        try:
            group = Group.objects.get(name=data['group'])
            user.groups.add(group)
            print(f"Usuario {data['username']} agregado al grupo {data['group']}")
        except Group.DoesNotExist:
            print(f"El grupo {data['group']} no existe")
    


create_user_roles_and_assign_permissions()
create_users_and_assign_groups()
add_states()