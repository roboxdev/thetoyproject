from django.contrib import admin

from blogging.models import Article, Writer


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticlesAdmin(admin.ModelAdmin):
    fields = (
        'created_at',
        'title',
        'content',
        'status',
        'written_by',
        'edited_by',
    )
    readonly_fields = (
        'created_at',
    )
