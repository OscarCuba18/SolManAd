from django.db import models
from .validators import validar_fecha_requerida, validar_descripcion

class State(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
# class State(models.TextChoices):
#     PENDIENTE = 'p', 'Pendiente'
#     EN_CURSO = 'ec', 'En curso'
#     TERMINADO = 't', 'Terminado'

class MaintenanceRequest(models.Model):
    user_id = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    date_requested = models.DateField(auto_now=True, auto_now_add=False)
    date_required = models.DateField(auto_now=False, auto_now_add=False, validators=[validar_fecha_requerida])
    description = models.TextField(validators=[validar_descripcion])
    state = models.ForeignKey("ticket.State", on_delete=models.CASCADE, default=1)
    # state = models.CharField(
    #         max_length=2,
    #         choices=State.choices,
    #         default=State.PENDIENTE
    #     )
    def __str__(self):
        return str(self.user_id.username) + str(self.date_requested) + str(self.date_required) + str(self.state)
    
class Assignament(models.Model):
    request_id = models.ForeignKey("ticket.MaintenanceRequest", on_delete=models.CASCADE)
    user_id = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    date_assigned = models.DateTimeField(auto_now=True, auto_now_add=False, validators=[validar_fecha_requerida])

