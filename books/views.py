from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import (
  LoginRequiredMixin, 
  PermissionRequiredMixin
)
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Book, Review


class BookListView(LoginRequiredMixin, ListView):
  model = Book
  context_object_name = "book_list"
  template_name = "books/book_list.html"
  login_url = "account_login"
  queryset = Book.objects.select_related().all().order_by("title")
  paginate_by = 9


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
  model = Book
  context_object_name = "book"
  template_name = "books/book_detail.html"
  login_url = "account_login"
  permission_required = "books.special_status"
  queryset = Book.objects.all().prefetch_related('reviews__author',)

class SearchResultsListView(LoginRequiredMixin, ListView):
  model = Book
  context_object_name = "book_list"
  template_name = "books/search_results.html"

  def get_queryset(self):
    query = self.request.GET.get("q")
    if query:
      return Book.objects.filter(
        Q(title__icontains=query) 
        | Q(author__icontains=query) 
        | Q(isbn__icontains=query)
        | Q(genre__icontains=query)
        | Q(publisher__icontains=query)
        | Q(description__icontains=query)
      ).distinct()
    return Book.objects.none()


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'isbn', 'description', 'published_date', 'publisher', 'pages', 'language', 'genre', 'price', 'cover']
    template_name = "books/book_form.html"
    login_url = "account_login"
    # permission_required = "books.special_status"
    success_url = reverse_lazy("book_list")

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['review', 'rating']
    template_name = "books/review_form.html"
    login_url = "account_login"

    def form_valid(self, form):
        form.instance.book = Book.objects.get(pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={"pk": self.kwargs['pk']})