from django.shortcuts import render
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# Create your views here.
class AuthorViewSet(viewsets.ModelViewSet):
    # queryset = Author.objects.all()
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    # queryset = Book.objects.all()
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["genre", "published_date"]
    search_fields = ["author_name"]

    def list(self, request, *args, **kargs):
        cache_key = "book_list"
        books = cache.get(cache_key)
        if not books:
            books = self.queryset
            serializer = self.get_serializer(books, many=True)
            cache.set(cache_key, serializer.data, timeout=60*15)
            return Response(serializer.data)
        return Response(books)
    
    def create(self, request, *args, **kargs):
        response = super().create(request, *args, **kargs)
        cache.delete('book_list')
        return response
    
    def update(self, request, *args, **kargs):
        response = super().update(request, *args, **kargs)
        cache.delete('book_list')
        return response
    
    def destroy(self, request, *args, **kargs):
        response = super().destroy(request, *args, **kargs)
        cache.delete('book_list')
        return response