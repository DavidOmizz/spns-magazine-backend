from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type',)

# admin.site.register(Contributor)
@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'contributor', 'edition', 'industry')

@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date',)

@admin.register(PDFRequest)
class PDFRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'requested_at')
