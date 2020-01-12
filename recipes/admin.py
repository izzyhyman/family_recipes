from django.contrib import admin

from .models import Recipe, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class RecipeAdmin(admin.ModelAdmin):
    inlines = [ CommentInline, ]
    list_display = ['title', 'ingredients', 'instructions', 'author', 'date']
    list_filter = ['author', 'date']
    search_fields = ['title', 'ingredients', 'instructions']
    date_hierarchy = 'date'
    ordering = ('date',)

admin.site.register(Recipe, RecipeAdmin)





