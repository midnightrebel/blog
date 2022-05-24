from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import  CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import *


class PostAdminForm(forms.ModelForm):
    сontent = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

class CommentAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Comment
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True
    list_display =  ('id','title','slug','createdAt','updatedAt','category','isPublished','views')
    list_display_links = ('id','title')
    search_fields = ('title',)
    list_filter = ('category','tags')
    readonly_fields = ('views','createdAt')


    def get_photo(self,obj):
        if obj.photo:
            return mark_safe(f'img src="{obj.photo.url}" width="50">')

class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class CommentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("authorComment",)}
    form = CommentAdminForm
    save_as = True

class CategorytAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category,CategorytAdmin)
admin.site.register(Tags,TagsAdmin)

admin.site.register(Comment,CommentAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Blog,BlogAdmin)
# Register your models here.
