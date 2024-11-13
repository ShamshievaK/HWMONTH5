from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies', null=False)
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()

    def __str__(self):
        return self.title

    @property
    def avarage_rating(self):
        return self.avarage_rating


stars = ((i, '*' * i) for i in range(1,6))


class Review(models.Model):
    text = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=stars, default=3)

    def __str__(self):
        return self.text

