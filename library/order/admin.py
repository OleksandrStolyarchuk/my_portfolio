from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'created_at', 'plated_end_at', 'end_at']

    fields = ['user', 'book', 'created_at', 'plated_end_at', 'end_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user', 'book', 'created_at', ]
        else:
            return ['created_at']

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.fieldsets = (
            (None, {
                'fields': ('user', 'book', 'created_at',)
            }),
            ('Editable', {
                'fields': ('plated_end_at', 'end_at')
            }),
        )
        return super(OrderAdmin, self).change_view(request, object_id)


admin.site.register(Order, OrderAdmin)
