from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Recipe


class RecipesViewTest(TestCase):
    def setUp(self):
        # Make a user for testing purposes
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="12345",
        )
        
        # Make a recipe object
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            ingredients="These are ingredients",
            instructions="Sample instructions.",
            author=self.user,
        )

    def test_about_page_status_code(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view(self):
        response = self.client.get("/recipes/1/")
        no_response = self.client.get("/recipes/1000000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Sample instructions.")
        self.assertTemplateUsed(response, "recipe_detail.html")

    def test_recipe_create_view(self):
        response = self.client.post(reverse('recipe_new'), {
            "title": "New title",
            "ingredients": "New ingredients",
            "instructions" : "New instructions",
            "author": self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New title")
        self.assertContains(response, "New ingredients")
        self.assertContains(response, "New instructions")

    def test_recipe_update_view(self):
        response = self.client.post(reverse('recipe_edit', args="1"), {
            "title": "Updated title",
            "ingredients": "Updated ingredients",
            "instructions" : "Updated instructions",
        })
        self.assertEqual(response.status_code, 302)

    def test_recipe_delete_view(self):
        response = self.client.get(reverse('recipe_delete', args="1"))
        self.assertEqual(response.status_code, 200)


class RecipeModelTest(TestCase):
    def setUp(self):
        # Make a user for testing purposes
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="12345",
        )
        
        # Make a recipe object
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            ingredients="These are ingredients",
            instructions="Sample instructions.",
            author=self.user,
        )

    def test_recipe_title(self):
        '''Ensure recipe title works.'''
        recipe1 = Recipe.objects.get(pk=1)
        expected_recipe_title = f"{recipe1.title}"
        self.assertEqual(expected_recipe_title, "Test Recipe")

    def test_recipe_ingredients(self):
        '''Ensure ingredients work'''
        recipe1 = Recipe.objects.get(pk=1)
        expected_recipe_ingredients = f"{recipe1.ingredients}"
        self.assertEqual(expected_recipe_ingredients, "These are ingredients")

    def test_recipe_instructions(self):
        '''Ensure instructions work'''
        recipe1 = Recipe.objects.get(pk=1)
        expected_recipe_instructions = f"{recipe1.instructions}"
        self.assertEqual(expected_recipe_instructions, "Sample instructions.")

    def test_recipe_author(self):
        '''Ensure the author is attached to the recipe'''
        recipe1 = Recipe.objects.get(pk=1)
        expected_author = get_user_model().objects.get(pk=1)
        self.assertEqual(expected_author.id, recipe1.author_id)

    def test_string_representation(self):
        recipe = Recipe(title="a sample title")
        self.assertEqual(str(recipe), recipe.title)

