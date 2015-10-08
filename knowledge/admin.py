from django.contrib import admin
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from knowledge.models import Question, Response, Category, Company, Author

def make_public(modeladmin, request, queryset):
    queryset.update(status='public')
make_public.short_description = "Mark selected articles public"

def make_rejected(modeladmin, request, queryset):
    queryset.update(status='rejected')
    for q in queryset:
        ctx = {
            'article': q.title,
            'email': q.email,
            'comment': q.comment,
        }
        #message = 'Your article: '+q.title+' has been rejected, Visit Portalpractices for more information'
        message = get_template('registration/article_rejected_template_email.html').render(Context(ctx))
        send_mail('Portalpractices: Article rejected', message, 'no-reply@cantemo.com', [q.email])
make_rejected.short_description = "Mark selected articles rejected"

def make_draft(modeladmin, request, queryset):
    queryset.update(status='draft')
make_draft.short_description = "Mark selected articles draft"

def make_review(modeladmin, request, queryset):
    queryset.update(status='review')
make_review.short_description = "Mark selected articles review"

def make_active(modeladmin, reqeust, queryset):
    queryset.update(is_active=True)
    for q in queryset:
        ctx = {
            'username': q.username,
            'email': q.email,
        }
        message = get_template('registration/activate_user_template_email.html').render(Context(ctx))
        send_mail('Portalpractices: Account activated', message, 'no-reply@cantemo.com', [q.email])
make_active.short_description = "Mark selected users active"

def make_author_active(modeladmin, reqeust, queryset):
    for query in queryset:
        query.user.is_active=True
        query.user.save(update_fields=['is_active'])
        ctx = {
            'username': query.user.username,
            'email': query.user.email,
        }
        message = get_template('registration/activate_user_template_email.html').render(Context(ctx))
        send_mail('Portalpractices: Account activated', message, 'no-reply@cantemo.com', [query.user.email])
make_active.short_description = "Mark selected users active"

class CategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]
    prepopulated_fields = {'slug': ('title', )}
admin.site.register(Category, CategoryAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'added', 'lastchanged', 'user', 'alert', 'name', 'email', 'title', 'comment', 'status', 'locked', 'recommended', 'hits'  )
    list_select_related = True
    list_filter = ['status']
    raw_id_fields = ['user']
    actions = [make_public, make_draft, make_review, make_rejected]
admin.site.register(Question, QuestionAdmin)

class ResponseAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Response._meta.fields]
    list_select_related = True
    raw_id_fields = ['user', 'question']
admin.site.register(Response, ResponseAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Company._meta.fields]
    list_select_related = True
    raw_id_fields = ['external_id']
admin.site.register(Company, CompanyAdmin)

class AuthorAdmin(admin.TabularInline):
    model = Author
#admin.site.register(Author, AuthorAdmin)

@receiver(pre_save, sender=User)
def send_user_email(sender, instance=None, **kwargs):
    old_instance = User.objects.get(pk=instance.pk)
    if old_instance.is_active == False and instance.is_active == True:
        ctx = {
            'username': instance.username,
            'email': instance.email,
        }
        message = get_template('registration/activate_user_template_email.html').render(Context(ctx))
        send_mail('Portalpractices: Account activated', message, 'no-reply@cantemo.com', [instance.email])

pre_save.connect(send_user_email, sender=User)

class UserAdmin(admin.ModelAdmin):
    inlines = [AuthorAdmin]
    actions = [make_active]
    list_filter = ['is_active']
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)