from django.contrib import admin

# Register your models here.
from petstagram.pets.models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'likes_count']
    # list_filter = ['name']
    # sortable_by = ['image_url']

    def likes_count(self, obj):
        return obj.like_set.count()


# admin.site.register(Pet, PetAdmin)