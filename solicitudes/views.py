from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404



def  llamar (elemento):

    return True

class ArticleViewSet(viewsets.ViewSet):
    

    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    def create(self, request):
        print (request.data)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)











