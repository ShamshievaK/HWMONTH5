from django.urls import path
from movie_app import views

urlpatterns = [
    # path('directors/', views.directors_list_create_api_view),
    # path('directors/<int:id>/', views.directors_detail_api_view),
    # path('movies/', views.movie_list_create_api_view),
    # path('movies/<int:id>/', views.movie_detail_api_view),
    # path('reviews/', views.review_list_create_api_view),
    # path('reviews/<int:id>/', views.review_detail_api_view),
    # path('', views.movie_review_api_view),
    path('directors/', views.DirectorListCreateAPIView.as_view()),
    # GENERIC Classes
    path('dir/', views.DirectorListAPIView.as_view()),
    path('dir/<int:id>/', views.DirectorDetailAPIView.as_view()),
    path('mov/', views.MovieListAPIView.as_view()),
    path('mov/<int:id>/', views.MovieDetailAPIView.as_view()),
    path('review/', views.ReviewListAPIView.as_view()),
    path('review/<int:id>/', views.ReviewDetailAPIView.as_view()),
    # ViewSet Classes
    path('direct/', views.DirectorViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('direct/<int:pk>/', views.DirectorViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    })),
    path('movrew/', views.MovieReviewAPIView.as_view()),
]