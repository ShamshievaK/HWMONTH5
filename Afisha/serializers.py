from audioop import avgpp

from rest_framework import serializers
from movie_app.models import Movie, Director, Review

class DirectorSerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()
    class Meta:
        model = Director
        fields = 'id name movie_count'.split()

    def get_movie_count(self, director):
        return director.movies.count()

class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'id title description duration director'.split()
        depth = 1


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie stars'.split()


class MovieReviewSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True, read_only=True, required=False)
    avarage_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description director duration review avarage_rating'.split()
        depth = 1

    def get_avarage_rating(self, movie):
        review = movie.reviews.all()
        if review:
            sum_review = sum(i.stars for i in review)
            avarage = sum_review / len(review)
            return avarage
        return None




# class MovieReviewSerializer(serializers.ModelSerializer):
#     reviews = ReviewSerializer(many=True, read_only=True)
#     average_rating = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Movie
#         fields = 'id movies_reviews reviews average_rating'.split()
#         depth = 1
#
#     def get_average_rating(self, obj):
#         if obj.reviews.count() > 0:
#             return obj.reviews.aggregate(avg=avgpp('stars'))['avg']
#         return None


