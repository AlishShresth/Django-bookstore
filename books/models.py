import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class Book(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=200)
  isbn = models.CharField("ISBN", max_length=13, unique=True, null=True, blank=True)
  description = models.TextField(null=True,blank=True)
  published_date = models.DateField(null=True, blank=True)
  publisher = models.CharField(max_length=200, blank=True)
  pages = models.PositiveIntegerField(null=True, blank=True)
  language = models.CharField(max_length=30, default="English")
  genre = models.CharField(max_length=100, blank=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  cover = models.ImageField(upload_to="covers/", blank=True)

  class Meta:
    indexes = [
      models.Index(fields=["id"], name="id_index"),
      models.Index(fields=["isbn"], name="isbn_index"),
    ]
    permissions = [
      ("special_status", "Can read all books"),
    ]

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse("book_detail", args=[str(self.id)])
  

class Review(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews",)
  review = models.TextField(max_length=1500)
  rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.review[:50]} - {self-rating}⭐"