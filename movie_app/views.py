from collections import OrderedDict
from multiprocessing.managers import Token
from symtable import Class

from django.contrib.auth import authenticate
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Director, Movie, Review
from movie_app.serializers import DirectorSerializer, DirectorDetailSerializer, MovieSerializer, MovieDetailSerializer, \
    ReviewSerializer, MovieReviewSerializer, MovieValidateSerializer, DirectorValidateSerializer, \
    ReviewValidateSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView



class DirectorViewSet(ModelViewSet):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()


class DirectorListAPIView(ListCreateAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    pagination_class = PageNumberPagination

class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorDetailSerializer
    queryset = Director.objects.all()
    lookup_field = 'id'

class MovieListAPIView(ListCreateAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = PageNumberPagination

class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.all()
    lookup_field = 'id'

class ReviewListAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'id'

class MovieReviewAPIView(APIView):
    def post(self, request):

        movies = Movie.objects.prefetch_related('reviews').all()
        data = MovieReviewSerializer(movies, many=True).data
        return Response(data=data)





# @api_view(['GET', 'POST'])
# def directors_list_create_api_view(request):
#     if request.method == 'GET':
#         directors = Director.objects.prefetch_related('movies').all()
#         data = DirectorSerializer(instance=directors, many=True).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = DirectorValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         name = serializer.validated_data.get('name')
#         director = Director.objects.create(name=name)    # 1 способ    # bulk_create-создает одним запросов несколько обьектов
#         # director = Director(name=name)
#         # Directoe(save) - 2 способ создания
#         return Response(status=status.HTTP_201_CREATED, data=DirectorSerializer(director).data)
#
#
#     # ДЛЯ GET ЗАПРОСА:
#     # ШАГ 1: СОБРАТЬ ПОЛУЧИТ СПИСОК
#     # ШАГ 2: ПРЕОБРОЗОВАТЬ (QUERYSET) СПИСОК В СЛОВАРЬ (QUERYDICT)
#     # ШАГ 3: ВЕРНУТЬ ОТВЕТ В ВИДЕ JSON
#
#     # ДЛЯ POST ЗАПРОСА:
#     # ШАГ 0: Проверить существует ли само значение и на типизацию(validation of data: Existing, Typing, Extra)
#     # ШАГ 1: получить данные от клиента (Receive data from RequestBody)
#     # ШАГ 2: с помощью полученных данных создаем (Create product by received data)
#     # ШАГ 3: отдаем ответ (Return Response (status, data))
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def directors_detail_api_view(request, id):
#     try:
#         directors = Director.objects.get(id=id)
#     except Director.DoesNotExist:
#         return Response(data={'error': 'Director does not found.'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = DirectorDetailSerializer(directors, many=False).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = DirectorValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         directors.name = serializer.validated_data.get('name')
#         directors.save()
#         return Response(status=status.HTTP_201_CREATED, data=DirectorDetailSerializer(directors).data)
#     elif request.method == 'DELETE':
#         directors.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET', 'POST'])
# def movie_list_create_api_view(request):
#     if request.method == 'GET':
#         movies = Movie.objects.select_related('director').prefetch_related('director', 'reviews').all()
#         data = MovieSerializer(movies, many=True).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = MovieValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
#         title = serializer.validated_data.get('title')
#         description = serializer.validated_data.get('description')
#         duration = serializer.validated_data.get('duration')
#         director_id = serializer.validated_data.get('director_id')  # При ForeygnKey испльзуй id\ При Many to many используй set (Например Movie.tags.set(tags) movie.save())
#         movies = Movie.objects.create(
#             title=title,
#             description=description,
#             duration=duration,
#             director_id=director_id
#         )
#         return Response(status=status.HTTP_201_CREATED, data=MovieSerializer(movies).data)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail_api_view(request, id):
#     try:
#         movies = Movie.objects.get(id=id)
#     except Movie.DoesNotExist:
#         return Response(data={'error': 'Movie does not found.'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = MovieDetailSerializer(movies, many=False).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = MovieValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         movies.title = serializer.validated_data.get('title')
#         movies.description = serializer.validated_data.get('description')
#         movies.duration = serializer.validated_data.get('duration')
#         movies.director_id = serializer.validated_data.get('director_id')
#         movies.save()
#         return Response(status=status.HTTP_201_CREATED, data=MovieDetailSerializer(movies).data)
#     elif request.method == 'DELETE':
#         movies.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET', 'POST'])
# def review_list_create_api_view(request):
#     if request.method == 'GET':
#         reviews = Review.objects.all()
#         data = ReviewSerializer(reviews, many=True).data
#         return Response(data=data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = ReviewValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         text = serializer.validated_data.get('text')
#         movie_id = serializer.validated_data.get('movie_id')
#         stars = serializer.validated_data.get('stars')
#         reviews = Review.objects.create(
#             text=text,
#             movie_id=movie_id,
#             stars=stars
#         )
#         return Response(status=status.HTTP_201_CREATED, data=ReviewSerializer(reviews).data)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def review_detail_api_view(request, id):
#     try:
#         reviews = Review.objects.get(id=id)
#     except Review.DoesNotExist:
#         return Response(data={'error': 'Review does not found.'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = ReviewSerializer(reviews, many=False).data
#         return Response(data=data)
#     elif request.method == 'PUT':
#         serializer = ReviewValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         reviews.text = serializer.validated_data.get('text')
#         reviews.movie_id = serializer.validated_data.get('movie_id')
#         reviews.stars = serializer.validated_data.get('stars')
#         reviews.save()
#         return Response(status=status.HTTP_201_CREATED, data=ReviewSerializer(reviews).data)
#     elif request.method == 'DELETE':
#         reviews.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)













