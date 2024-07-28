from django.db import models
from .validators import validar_img_format, validar_mp4

class Comment(models.Model):
    request_id = models.ForeignKey("ticket.MaintenanceRequest", on_delete=models.CASCADE)
    user_id = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ImageField(upload_to='comments/images/', blank=True, null=True, validators=[validar_img_format])
    video = models.FileField(upload_to='comments/videos/', blank=True, null=True, validators=[validar_mp4])

    def __str__(self):
        return self.comment
    