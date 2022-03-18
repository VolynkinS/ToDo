from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True


admin.site.register(Todo, TodoAdmin)
