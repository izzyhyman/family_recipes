from django.urls import path

from .views import (
    recipe_detail_view,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    RecipeListView,
    SearchResultsListView,
)

urlpatterns = [
    path("<int:pk>/", recipe_detail_view, name="recipe_detail"),
    path('new/', RecipeCreateView.as_view(), name="recipe_new"),
    path('<int:pk>/edit/', RecipeUpdateView.as_view(), name="recipe_edit"),
    path('<int:pk>/delete/', RecipeDeleteView.as_view(), name="recipe_delete"),
    path('search/', SearchResultsListView.as_view(), name="search_results"),
]