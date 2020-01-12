
from django.conf import settings
from django.conf.urls.static  import static
from django.contrib import admin
from django.urls import path, include

from recipes.views import RecipeListView
from pages.views import AboutPageView

urlpatterns = [
    path('all-about-admin/', admin.site.urls),
    path("", RecipeListView.as_view(), name="recipe_list"),
    path("about/", AboutPageView.as_view(), name="about"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('recipes/', include('recipes.urls')),
]

if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

