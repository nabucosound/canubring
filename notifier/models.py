from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives

from boto.exception import BotoServerError


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    creation_dt = models.DateTimeField(auto_now_add=True)
    displayed = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)


class NotificationMixin(object):
    """
    Adds methods to deliver email.
    """
    email_subject_tmpl = None
    email_plaintext_body_tmpl = None
    email_html_body_tmpl = None
    from_email = settings.DEFAULT_FROM_EMAIL

    def _render_tmpl(self, template):
        from django.utils import translation
        ctxt = self.get_context()
        site = Site.objects.get(id=settings.SITE_ID)
        ctxt['site'] = "http://%s" % site.domain
        ctxt['LANGUAGE_CODE'] = translation.get_language()
        return render_to_string(template, ctxt)

    def get_context(self):
        return {}

    def _get_email_field(self, attr_name, method_name):
        template = getattr(self, attr_name, None)
        if template is None:
            raise ImproperlyConfigured(u"%(cls)s is missing a "
                u"template. Define %(cls)s.%(attr)s, or override "
                u"%(cls)s.%(method_name)s()." % {'attr': attr_name, "cls": self.__class__.__name__, 'method_name': method_name,
            })
        return self._render_tmpl(template)

    def get_email_subject(self):
        return self._get_email_field('email_subject_tmpl', 'get_email_subject')

    def get_email_plaintext_body(self):
        return self._get_email_field('email_plaintext_body_tmpl', 'get_email_plaintext_body')

    def get_email_html_body(self):
        try:
            return self._get_email_field('email_html_body_tmpl', 'get_email_html_body')
        except ImproperlyConfigured:
            return None

    def get_from_email(self):
        return self.from_email

    def get_email_headers(self):
        raise NotImplementedError  # Must be implemented by class using mixin

    def get_recipients_list(self):
        raise NotImplementedError  # Must be implemented by class using mixin

    def send_notification_email(self):
        if getattr(settings, 'SEND_EMAIL_NOTIFICATIONS', False):
            from_email = self.get_from_email()
            headers = self.get_email_headers()
            recipients = self.get_recipients_list()
            subject = self.get_email_subject().strip()
            plaintext_body = self.get_email_plaintext_body()
            msg = EmailMultiAlternatives(subject, plaintext_body, from_email, recipients, headers=headers)
            html_body = self.get_email_html_body()
            if html_body:
                msg.attach_alternative(html_body, 'text/html')
            try:
                msg.send()
            except BotoServerError:
                # 400 Bad Request
                # Examples: InvalidParameterValue (Missing final '@domain')
                pass
            self.email_sent = True
            self.save()

