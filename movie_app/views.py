from sre_constants import error

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from Afisha.serializers import DirectorSerializer, DirectorDetailSerializer, MovieSerializer, MovieDetailSerializer, \
    ReviewSerializer, MovieReviewSerializer


@api_view(['GET', 'POST'])
def directors_list_create_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.prefetch_related('movies').all()
        data = DirectorSerializer(instance=directors, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        name = request.data.get('name')
        director = Director.objects.create(name=name)    # 1 способ    # bulk_create-создает одним запросов несколько обьектов
        # director = Director(name=name)
        # Directoe(save) - 2 способ создания
        return Response(status=status.HTTP_201_CREATED, data=DirectorSerializer(director).data)

    # ДЛЯ GET ЗАПРОСА:
    # ШАГ 1: СОБРАТЬ ПОЛУЧИТ СПИСОК
    # ШАГ 2: ПРЕОБРОЗОВАТЬ (QUERYSET) СПИСОК В СЛОВАРЬ (QUERYDICT)
    # ШАГ 3: ВЕРНУТЬ ОТВЕТ В ВИДЕ JSON

    # ДЛЯ POST ЗАПРОСА:
    # ШАГ 1: получить данные от клиента (Receive data from RequestBody)
    # ШАГ 2: с помощью полученных данных создаем (Create product by received data)
    # ШАГ 3: отдаем ответ (Return Response (status, data))
@api_view(['GET', 'PUT', 'DELETE'])
def directors_detail_api_view(request, id):
    try:
        directors = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director does not found.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = DirectorDetailSerializer(directors, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        directors.name = request.data.get('name')
        directors.save()
        return Response(status=status.HTTP_201_CREATED, data=DirectorDetailSerializer(directors).data)
    elif request.method == 'DELETE':
        directors.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def movie_list_create_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.select_related('director').prefetch_related('director', 'reviews').all()
        data = MovieSerializer(movies, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')  # При ForeygnKey испльзуй id\ При Many to many используй set (Например Movie.tags.set(tags) movie.save())
        movies = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director_id=director_id
        )
        return Response(status=status.HTTP_201_CREATED, data=MovieSerializer(movies).data)

@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movies = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie does not found.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieDetailSerializer(movies, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        movies.title = request.data.get('title')
        movies.description = request.data.get('description')
        movies.duration = request.data.get('duration')
        movies.director_id = request.data.get('director_id')
        movies.save()
        return Response(status=status.HTTP_201_CREATED, data=MovieDetailSerializer(movies).data)
    elif request.method == 'DELETE':
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.data.get('text')
        movie_id = request.data.get('movie_id')
        stars = request.data.get('stars')
        reviews = Review.objects.create(
            text=text,
            movie_id=movie_id,
            stars=stars
        )
        return Response(status=status.HTTP_201_CREATED, data=ReviewSerializer(reviews).data)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        reviews = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review does not found.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewSerializer(reviews, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        reviews.text = request.data.get('text')
        reviews.movie_id = request.data.get('movie_id')
        reviews.stars = request.data.get('stars')
        reviews.save()
        return Response(status=status.HTTP_201_CREATED, data=ReviewSerializer(reviews).data)
    elif request.method == 'DELETE':
        reviews.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def movie_review_api_view(request):
    movies = Movie.objects.prefetch_related('reviews').all()
    data = MovieReviewSerializer(movies, many=True).data
    return Response(data=data)




