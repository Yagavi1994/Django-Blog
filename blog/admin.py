from django.contrib import admin
from django.db.models import Q
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, CATEGORY, GENRES, Comment

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'get_category_display', 'get_genre_display', 'status')
    list_filter = ('status', 'category', 'genre', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
    search_fields = ['title']

    def get_search_results(self, request, queryset, search_term):
        """
        Overrides the default search behavior to enable searching by
        category name and genre name.
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Convert the search term to lowercase
        search_term = search_term.lower()

        # Mapping for category and genre names to their corresponding integer values
        category_mapping = {name.lower(): value for value, name in CATEGORY}
        genre_mapping = {name.lower(): value for value, name in GENRES}

        # Check if the search term matches any category or genre name
        if search_term in category_mapping:
            queryset |= self.model.objects.filter(category=category_mapping[search_term])
        
        if search_term in genre_mapping:
            queryset |= self.model.objects.filter(genre=genre_mapping[search_term])

        return queryset, use_distinct

    def get_category_display(self, obj):
        return dict(CATEGORY).get(obj.category)

    def get_genre_display(self, obj):
        return dict(GENRES).get(obj.genre)

    get_category_display.short_description = 'Category'
    get_genre_display.short_description = 'Genre'



    
# Register your models here.

admin.site.register(Comment)
