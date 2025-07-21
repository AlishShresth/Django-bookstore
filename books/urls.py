from django.urls import path

from .views import BookListView, BookDetailView, SearchResultsListView, BookCreateView, ReviewCreateView


urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<uuid:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path("new/", BookCreateView.as_view(), name="book_create"),
    path("<uuid:pk>/review/", ReviewCreateView.as_view(), name="review_create"),
]
