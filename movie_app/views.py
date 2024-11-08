from sre_constants import error

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from Afisha.serializers import DirectorSerializer, DirectorDetailSerializer, MovieSerializer, MovieDetailSerializer, \
    ReviewSerializer


@api_view(['GET'])
def directors_list_api_view(request):
    # ШАГ 1: СОБРАТЬ ПОЛУЧИТ СПИСОК
    directors = Director.objects.all()
    # ШАГ 2: ПРЕОБРОЗОВАТЬ (QUERYSET) СПИСОК В СЛОВАРЬ (QUERYDICT)
    data = DirectorSerializer(instance=directors, many=True).data
    # ШАГ 3: ВЕРНУТЬ ОТВЕТ В ВИДЕ JSON
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def directors_detail_api_view(request, id):
    try:
        directors = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director does not found.'}, status=status.HTTP_404_NOT_FOUND)
    data = DirectorDetailSerializer(directors, many=False).data
    return Response(data=data)


@api_view(['GET'])
def movie_list_api_view(request):
    movies = Movie.objects.all()
    data = MovieSerializer(movies, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def movie_detail_api_view(request, id):
    try:
        movies = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie does not found.'}, status=status.HTTP_404_NOT_FOUND)
    data = MovieDetailSerializer(movies, many=False).data
    return Response(data=data)

@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(reviews, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        reviews = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review does not found.'}, status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(reviews, many=False).data
    return Response(data=data)


