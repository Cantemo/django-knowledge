from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

class CustomRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):

    """
        Based on RelatedFieldWidgetWrapper, this does the same thing
        outside of the admin interface

        the parameters for a relation and the admin site are replaced
        by a url for the add operation
    """

    def __init__(self, widget, add_url,permission=True):
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.widget = widget
        self.add_url = add_url
        self.permission = permission

    def render(self, name, value, *args, **kwargs):
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        if self.permission:
            output.append(u'<a href="%s" class="add-another" id="add_id_%s"> ' % \
                (self.add_url, name))
            output.append(u'<img src="%simg/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % ('/static/admin/', 'Add Another'))
        return mark_safe(u''.join(output))
