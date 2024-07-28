from django.shortcuts import render
from .serializers import CommentSerializer
from rest_framework import viewsets
from .models import Comment

class Comment_ViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
