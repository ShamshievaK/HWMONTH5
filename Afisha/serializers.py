from rest_framework import serializers
from movie_app.models import Movie, Director, Review
from rest_framework.exceptions import ValidationError

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


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True, min_length=10, max_length=100)
    director_id = serializers.IntegerField()
    duration = serializers.IntegerField()

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except:
            raise ValidationError('Director does not exist')
        return director_id

    def validate_title(self, title):
        try:
            Movie.objects.get(title=title)
            raise ValidationError('Такое название уже есть')
        except Movie.DoesNotExist:
            pass
        return title


    # def validate(self, attrs):
    #     director_id = attrs['director_id']
    #     try:
    #         Director.objects.get(id=director_id)
    #     except Director.DoesNotExist:
    #         raise ValidationError('Director does not exist')
    #     return attrs

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    stars = serializers.IntegerField()
    movie_id = serializers.IntegerField()

class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)




