from django.urls import path
from .views import TagsView, CategoriesView

app_name = 'characteristics'

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='all_categories'),
    path('tags', TagsView.as_view(), name='all_tags'),
]