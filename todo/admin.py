from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'datecompleted', 'user')
    list_display_links = ('title', 'created', 'datecompleted', 'user')
    readonly_fields = ('created',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    save_on_top = True


admin.site.register(Todo, TodoAdmin)
