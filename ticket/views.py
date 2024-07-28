from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import MaintenanceRequest, Assignament, State
from comment.models import Comment
from .form import Maintenance_Request_Form
from comment.form import CommentForm
from rest_framework import viewsets
from .serializers import MaintenanceRequest_Serializer, Assignament_Serializer

def is_solicitante(user):
    return user.groups.filter(name='Solicitante').exists()
def is_encargado(user):
    return user.groups.filter(name='EncargadoMantenimiento').exists()
def is_personal(user):
    return user.groups.filter(name='PersonalMantenimiento').exists()
def user_in_groups(user):
    return user.groups.filter(name__in=['Solicitante', 'EncargadoMantenimiento', 'PersonalMantenimiento']).exists()


@login_required
def List_Maitenance_Requests(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    
    if 'Solicitante' in user_groups:
        # Mostrar solicitudes creadas por el solicitante
        maintenance_requests = MaintenanceRequest.objects.filter(user_id=user)
    elif 'EncargadoMantenimiento' in user_groups:
        # Mostrar todas las solicitudes para el encargado de mantenimiento
        maintenance_requests = MaintenanceRequest.objects.all()
    elif 'PersonalMantenimiento' in user_groups:
        # Mostrar solicitudes asignadas al personal de mantenimiento
        maintenance_requests = MaintenanceRequest.objects.filter(assignament__user_id=user).order_by('-state').order_by('date_required')
    else:
        maintenance_requests = MaintenanceRequest.objects.none()

    return render(request, "Maintenance_Requests.html", {
        "Maintenance_Requests": maintenance_requests,
        "is_solicitante": 'Solicitante' in user_groups,
        "is_encargado": 'EncargadoMantenimiento' in user_groups,
        "is_personal": 'PersonalMantenimiento' in user_groups,
    })

# Crear solicitud para mantenimiento
@user_passes_test(is_solicitante)
def Maintenance_Request_FormView(request):
    maintenance_request = None
    id_maintenance_request = request.GET.get("id")
    
    if id_maintenance_request:
        maintenance_request = get_object_or_404(MaintenanceRequest, id=id_maintenance_request)
        form = Maintenance_Request_Form(instance=maintenance_request)
    else:
        form = Maintenance_Request_Form()
    
    if request.method == "POST":
        if maintenance_request:
            form = Maintenance_Request_Form(request.POST, instance=maintenance_request)
        else:
            form = Maintenance_Request_Form(request.POST)
        
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.user_id = request.user
            maintenance_request.state = State.objects.get(id=1)
            maintenance_request.save()
            return redirect('listar_solicitudes')
    
    return render(request, "form_Maintenance_Request.html", {"form": form})

# Asignar solicitud a un personal de mantenimiento
@user_passes_test(is_encargado)
def Assign_Maintenance_Request_FormView(request, id):
    maintenance_request = get_object_or_404(MaintenanceRequest, id=id)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        Assignament.objects.create(request_id=maintenance_request, user_id=user)
        maintenance_request.state = get_object_or_404(State, id=2)
        maintenance_request.save()
        return redirect('listar_solicitudes')

@login_required
@user_passes_test(user_in_groups)
def detail_request(request, id):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    maintenance_request = get_object_or_404(MaintenanceRequest, id=id)
    try:
        assignament = Assignament.objects.get(request_id=maintenance_request)
    except Assignament.DoesNotExist:
        assignament = None
    comments = Comment.objects.filter(request_id=maintenance_request)
    exist_comments = comments.exists()
    comment_form = CommentForm(request.POST or None, request.FILES or None)
    finalized_state = get_object_or_404(State, id=3)

    if finalized_state == maintenance_request.state:
        assignament = get_object_or_404(Assignament, request_id=maintenance_request)
        return render(request, 'detail_request.html', {
            'maintenance_request': maintenance_request, 
            'comments': comments, 'comment_form': comment_form, 
            'is_encargado': 'EncargadoMantenimiento' in user_groups,
            'is_personal': 'PersonalMantenimiento' in user_groups, 
            'is_finalizado': finalized_state, 
            'assignament': assignament,
            'exist_comments': exist_comments})

    if request.method == 'POST':
        if 'finalizar' in request.POST:
            maintenance_request.state = finalized_state
            maintenance_request.save()
            return redirect('listar_solicitudes')

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.request_id = maintenance_request
            comment.user_id = request.user
            comment.save()
            return redirect('detalle_solicitud', id=id)
    
    personal_mantenimiento_group = get_object_or_404(Group, name='PersonalMantenimiento')
    personalesMantenimiento = User.objects.filter(groups=personal_mantenimiento_group)

    return render(request, 'detail_request.html', {
        'maintenance_request': maintenance_request, 
        'comments': comments, 
        'comment_form': comment_form, 
        'is_encargado': 'EncargadoMantenimiento' in user_groups,
        'is_personal': 'PersonalMantenimiento' in user_groups, 
        'personalesMantenimiento': personalesMantenimiento, 
        'assignament': assignament,
        'exist_comments': exist_comments})

#-----------------------        API         -----------------------#
class MaintenanceRequest_ViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequest_Serializer
    permission_classes = [IsAuthenticated]

class Assignament_ViewSet(viewsets.ModelViewSet):
    queryset = Assignament.objects.all()
    serializer_class = Assignament_Serializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def maintenance_request_count(request):
    """
    Cuenta la cantidad de __maintenance_requests__
    """

    try:
        solicitudes = MaintenanceRequest.objects.count()
        return JsonResponse(
            {
                "cantidad": solicitudes
            },
            safe=False,
            status=200,
        )
    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            safe=False,
            status=400
        )

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  # Redirige al usuario autenticado si ya ha iniciado sesión

class CustomLogoutView(LogoutView):
    template_name = 'logged_out.html'