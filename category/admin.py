from django.contrib import admin
from .models import Category

    

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)} # Auto-fill slug in admin
    list_display = ('category_name', 'slug')  # Display both fields in admin


admin.site.register(Category, CategoryAdmin)


