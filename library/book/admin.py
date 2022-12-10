from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from .models import Book
from author.models import Author


class AuthorInline(admin.StackedInline):
    model = Author.books.through
    verbose_name = 'Authors'

    def has_change_permission(self, request, obj=None):
        return False

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        else:
            return 1


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'description', 'count', 'publication_year', 'date_of_issue']
    list_filter = ['id', 'name', 'authors']

    inlines = [AuthorInline]
    fields = ['name', 'description', 'count', 'publication_year', 'date_of_issue']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['name', 'description', 'count', 'publication_year']
        else:
            return []

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.fieldsets = (
            (None, {
                'fields': ('name', 'description', 'count', 'publication_year',)
            }),
            ('Editable', {
                'fields': ('date_of_issue',)
            }),
        )
        return super(BookAdmin, self).change_view(request, object_id)

    @admin.display(description='Authors')
    def author(self, obj):
        return [author for author in obj.authors.all()]


admin.site.register(Book, BookAdmin)
