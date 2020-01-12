from django.shortcuts import redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormMixin
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q

from .models import Recipe

from .forms import CommentForm, RecipeForm


class RecipeListView(ListView):
    '''list recipes on the home page'''
    model = Recipe
    template_name = "recipe_list.html"
    context_object_name = "all_recipes_list"
    paginate_by = 4

# Finish rewriting this view
def recipe_detail_view(request, pk):
    template_name = "recipe_detail"
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all()

    new_comment = None

    # receiving a comment via post method
    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(data=request.POST)

        # check to see if the form has valid data
        if comment_form.is_valid():
            # create the comment object, but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.recipe = recipe
            # save to the database
            new_comment.save()
            # redirect to new URL
            messages.add_message(request, messages.SUCCESS, "New comment added!", extra_tags="success")
            return redirect(recipe)

    else:
        # must be a get method
        comment_form = CommentForm()
    context = {
        "recipe": recipe,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "recipe_detail.html", context)



class RecipeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Recipe
    template_name = 'recipe_new.html'
    login_url = 'login'
    context_object_name = 'recipe'
    form_class = RecipeForm
    success_url = reverse_lazy("recipe_list")
    success_message = "New recipe created!"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    template_name = 'recipe_edit.html'
    fields = ['title', 'ingredients', 'instructions', 'image']
    login_url = "login"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipe_delete.html'
    success_url = reverse_lazy('recipe_list')
    login_url = "login"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class SearchResultsListView(ListView):
    # model = Recipe
    context_object_name = 'all_recipes_list'
    template_name = 'search_results.html'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Recipe.objects.filter(
            Q(title__icontains=query)|Q(ingredients__icontains=query)|Q(instructions__icontains=query)
        )

    