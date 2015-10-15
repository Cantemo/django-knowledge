from knowledge import settings

import django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings
from knowledge.managers import QuestionManager, ResponseManager
from knowledge.signals import knowledge_post_save
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode
from taggit.managers import TaggableManager

STATUSES = (
    ('public', _('Public')),
    ('draft', _('Draft')),
    ('review', _('Review')),
    ('rejected', _('Rejected')),
)


STATUSES_EXTENDED = STATUSES + (
    ('inherit', _('Inherit')),
)


class Category(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    lastchanged = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class KnowledgeBase(models.Model):
    """
    The base class for Knowledge models.
    """
    is_question, is_response = False, False

    added = models.DateTimeField(auto_now_add=True)
    lastchanged = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('auth.User' if django.VERSION < (1, 5, 0) else django_settings.AUTH_USER_MODEL, blank=False,
                             null=True, db_index=True)
    alert = models.BooleanField(default=settings.ALERTS,
        verbose_name=_('Alert'),
        help_text=_('Check this if you want to be alerted when a new'
                        ' response is added.'))

    # for anonymous posting, if permitted
    name = models.CharField(max_length=64, blank=True, null=True,
        verbose_name=_('Name'),
        help_text=_('Enter your first and last name.'))
    email = models.EmailField(blank=True, null=True,
        verbose_name=_('Email'),
        help_text=_('Enter a valid email address.'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.user and self.name and self.email \
                and not self.id:
            # first time because no id
            self.public(save=False)

        if settings.AUTO_PUBLICIZE and not self.id:
            self.public(save=False)

        super(KnowledgeBase, self).save(*args, **kwargs)

    #########################
    #### GENERIC GETTERS ####
    #########################

    def get_name(self):
        """
        Get local name, then self.user's first/last, and finally
        their username if all else fails.
        """
        name = (self.name or (self.user and (
            u'{0} {1}'.format(self.user.first_name, self.user.last_name).strip()\
            or self.user.username
        )))
        return name.strip() or _("Anonymous")

    get_email = lambda s: s.email or (s.user and s.user.email)
    get_pair = lambda s: (s.get_name(), s.get_email())
    get_user_or_pair = lambda s: s.user or s.get_pair()

    ########################
    #### STATUS METHODS ####
    ########################

    def can_view(self, user):
        """
        Returns a boolean dictating if a User like instance can
        view the current Model instance.
        """
        if self.status == 'inherit' and self.is_response:
            return self.question.can_view(user)

        if self.status == 'rejected' and user.is_staff:
            return True
        
        if self.status == 'review' and user.is_staff: 
            return True

        if self.status == 'draft':
            if self.user == user or user.is_staff:
                return True
            if self.is_response and self.question.user == user: 
                return True

        if self.status == 'public': 
            return True

        return False

    def switch(self, status, save=True):
        self.status = status
        if save:
            self.save()
    switch.alters_data = True

    def public(self, save=True):
        self.switch('public', save)
    public.alters_data = True

    def draft(self, save=True):
        self.switch('draft', save)
    draft.alters_data = True

    def inherit(self, save=True):
        self.switch('inherit', save)
    inherit.alters_data = True

    def review(self, save=True):
        self.switch('review', save)
    review.alters_data = True

    def rejected(self, save=True):
        self.switch('rejected', save)
    rejected.alters_data = True

class Company(models.Model):
    """ We could have multiple people per company I suppose, 
        so Company could be what we show some information on?
    """
    name = models.CharField(max_length=255, blank=False)
    external_id = models.ForeignKey('auth.User', default=False, related_name='user_company', help_text=_('ID of the user that will own the company.'))
    nickname = models.CharField(_('nickname'), max_length=50, blank=True, null=True)
    about = RichTextField(_('about'), blank=True, null=True)
    web_site = models.URLField(_('URL'))
    location = models.CharField(max_length=255, blank=False)
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)
    is_deleted = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='uploads/avatars/', default ='uploads/avatars/default.jpg')

    class Meta:
        ordering = ('name',)
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    def __unicode__(self):
        return force_unicode(self.name)
    
    def get_admin_url(self):
        return reverse('admin:%s_%s_change' %(self._meta.app_label, self._meta.module_name), args=[self.id])
    
    def get_name(self):
        return force_unicode(self.name)

class Author(models.Model):
    """ Author extends User to give a little more information """
    user = models.OneToOneField(User, related_name='user_author') 
    company = models.ForeignKey(Company, null=True)
    title = models.CharField(_('title'), max_length=200, blank=True)
    about = models.TextField(_('about'), blank=True, null=True)
    avatar = models.ImageField(upload_to='uploads/avatars-author/', default ='uploads/avatars-author/default.jpg')
    
    class Meta:
        ordering = ('user',)
        verbose_name = _('Author')
        verbose_name_plural = _('Author') 
    
    def __unicode__(self):
        return force_unicode(self.fullname)
        
    @property
    def fullname(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)
        
class Question(KnowledgeBase):
    is_question = True
    _requesting_user = None

    title = models.CharField(max_length=255,
        verbose_name=_('Title'))
    body = RichTextField(blank=True, null=True,
        verbose_name=_('Body'))

    summary = models.CharField(default='',
        max_length=255, verbose_name=_('Summary'))

    comment = models.CharField(blank=True, null=True,
        verbose_name=_('Comment'), max_length=455)

    status = models.CharField(
        verbose_name=_('Status'),
        max_length=32, choices=STATUSES,
        default='review', db_index=True)

    picture = models.ImageField(upload_to='uploads/article-picture/', null=True, blank=True)

    locked = models.BooleanField(default=False)

    recommended = models.BooleanField(default=False)

    hits = models.PositiveIntegerField(default=0)

    categories = models.ManyToManyField('knowledge.Category', blank=True)

    tags = TaggableManager(blank=True)

    objects = QuestionManager()

    def private(self, save=True):
        self.switch('draft', save)
    private.alters_data = True

    class Meta:
        ordering = ['-added']
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __unicode__(self):
        return self.title
        
    def get_company_logo(self):
        author = Author.objects.get(user=self.user)
        company_instance = Company.objects.get(name=author.company)
        return company_instance.avatar

    @models.permalink
    def get_absolute_url(self):
        from django.template.defaultfilters import slugify

        if settings.SLUG_URLS:
            return ('knowledge_thread', [self.id, slugify(self.title)])
        else:
            return ('knowledge_thread_no_slug', [self.id])

    def inherit(self):
        pass

    def review(self):
        pass

    def rejected(self):
        pass

    def lock(self, save=True):
        self.locked = not self.locked
        if save:
            self.save()
    lock.alters_data = True

    ###################
    #### RESPONSES ####
    ###################

    def get_responses(self, user=None):
        user = user or self._requesting_user
        if user:
            return [r for r in self.responses.all().select_related('user') if r.can_view(user)]
        else:
            return self.responses.all().select_related('user')

    def answered(self):
        """
        Returns a boolean indictating whether there any questions.
        """
        return bool(self.get_responses())

    def accepted(self):
        """
        Returns a boolean indictating whether there is a accepted answer
        or not.
        """
        return any([r.accepted for r in self.get_responses()])

    def clear_accepted(self):
        self.get_responses().update(accepted=False)
    clear_accepted.alters_data = True

    def accept(self, response=None):
        """
        Given a response, make that the one and only accepted answer.
        Similar to StackOverflow.
        """
        self.clear_accepted()

        if response and response.question == self:
            response.accepted = True
            response.save()
            return True
        else:
            return False
    accept.alters_data = True

    def states(self):
        """
        Handy for checking for mod bar button state.
        """
        return [self.status, 'lock' if self.locked else None]

    @property
    def url(self):
        return self.get_absolute_url()

    def get_question_company(self):
        author_instance = Author.objects.get(user=self.user)
        return author_instance.company

    def get_question_first_name(self):
        user_instance = User.objects.get(username=self.user)
        return user_instance.first_name

    def get_question_last_name(self):
        user_instance = User.objects.get(username=self.user)
        return user_instance.last_name


class Response(KnowledgeBase):
    is_response = True

    question = models.ForeignKey('knowledge.Question',
        related_name='responses')

    body = RichTextField(blank=True, null=True,
        verbose_name=_('Response'),
        help_text=_('Please enter your response.'))
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=32, choices=STATUSES_EXTENDED,
        default='inherit', db_index=True)
    accepted = models.BooleanField(default=False)

    objects = ResponseManager()

    class Meta:
        ordering = ['added']
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')

    def __unicode__(self):
        return self.body[0:100] + u'...'

    def states(self):
        """
        Handy for checking for mod bar button state.
        """
        return [self.status, 'accept' if self.accepted else None]

    def accept(self):
        self.question.accept(self)
    accept.alters_data = True


# cannot attach on abstract = True... derp
models.signals.post_save.connect(knowledge_post_save, sender=Question)
models.signals.post_save.connect(knowledge_post_save, sender=Response)
