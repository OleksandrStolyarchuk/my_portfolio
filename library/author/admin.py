from django.contrib import admin

from .models import Author


class BookInline(admin.StackedInline):
    model = Author.books.through

    def has_change_permission(self, request, obj=None):
        return False

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ['name', 'surname', 'patronymic', 'book']
    fields = [('name', 'surname'), 'patronymic']

    @admin.display(description='Books')
    def book(self, obj):
        return [book.name for book in obj.books.all()]


admin.site.register(Author, AuthorAdmin)
