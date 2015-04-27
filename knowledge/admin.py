
from django.contrib import admin

from knowledge.models import Question, Response, Category
from portalpractices.models import Company, Author

def make_public(modeladmin, request, queryset):
    queryset.update(status='public')
make_public.short_description = "Mark selected articles public"

def make_rejected(modeladmin, request, queryset):
    queryset.update(status='rejected')
make_rejected.short_description = "Mark selected articles rejected"

def make_draft(modeladmin, request, queryset):
    queryset.update(status='draft')
make_draft.short_description = "Mark selected articles draft"

def make_review(modeladmin, request, queryset):
    queryset.update(status='review')
make_review.short_description = "Mark selected articles review"

class CategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]
    prepopulated_fields = {'slug': ('title', )}
admin.site.register(Category, CategoryAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Question._meta.fields]
    list_select_related = True
    list_filter = ['status']
    raw_id_fields = ['user']
    actions = [make_public, make_draft, make_review, make_rejected]
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
