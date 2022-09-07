# from django.shortcuts import render
# Create your views here.

from rest_framework import viewsets

from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
