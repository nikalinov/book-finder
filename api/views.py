from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()

        sort = self.request.query_params.get('sort')
        if sort:  # if sorting == 'rating'
            queryset = queryset.order_by('-' + sort)

        filt = self.request.query_params.get('filter')
        if filt:  # filter by non-zero reviews
            queryset = queryset.filter(rating__isnull=False)

        return queryset


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

