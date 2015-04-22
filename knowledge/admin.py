
from django.contrib import admin

from knowledge.models import Question, Response, Category
from portalpractices.models import Company, Author


class CategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]
    prepopulated_fields = {'slug': ('title', )}
admin.site.register(Category, CategoryAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Question._meta.fields]
    list_select_related = True
    raw_id_fields = ['user']
admin.site.register(Question, QuestionAdmin)

class CompanyAdmin(admin.ModelAdmin):
 list_display = [f.name for f in Company._meta.fields]
 list_select_related = True
 raw_id_fields = ['external_id']
admin.site.register(Company, CompanyAdmin)

class AuthorAdmin(admin.ModelAdmin):
 list_display = [f.name for f in Author._meta.fields]
 list_select_related = True
 raw_id_fields = ['company']
admin.site.register(Author, AuthorAdmin)

class ResponseAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Response._meta.fields]
    list_select_related = True
    raw_id_fields = ['user', 'question']
admin.site.register(Response, ResponseAdmin)
