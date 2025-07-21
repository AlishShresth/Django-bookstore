from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import (
  LoginRequiredMixin, 
  PermissionRequiredMixin
)
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


from .models import Book, Review


class BookListView(LoginRequiredMixin, ListView):
  model = Book
  context_object_name = "book_list"
  template_name = "books/book_list.html"
  login_url = "account_login"
  queryset = Book.objects.select_related().all().order_by("title")
  paginate_by = 9


class BookDetailView(LoginRequiredMixin, DetailView):
  model = Book
  context_object_name = "book"
  template_name = "books/book_detail.html"
  login_url = "account_login"
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


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'isbn', 'description', 'published_date', 'publisher', 'pages', 'language', 'genre', 'price', 'cover']
    template_name = "books/book_form.html"
    login_url = "account_login"
    success_url = reverse_lazy("book_list")

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['review', 'rating']
    template_name = "books/review_form.html"
    login_url = "account_login"

    def dispatch(self, request, *args, **kwargs):
        # Fetch the book once and store it for reuse
        self.book = get_object_or_404(Book, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.book = self.book
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context

    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={"pk": self.kwargs['pk']})