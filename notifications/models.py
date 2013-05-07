from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User

from notifier.models import Notification, NotificationMixin
from cargos.models import CargoComment, Cargo


class WelcomeNotification(Notification, NotificationMixin):
    obj = models.ForeignKey(User)

    from_email = settings.DEFAULT_FROM_EMAIL
    email_subject_tmpl = 'emails/welcome_noti_subject.txt'
    email_plaintext_body_tmpl = 'emails/welcome_noti_plaintext_body.txt'
    email_html_body_tmpl = 'emails/welcome_noti_html_body.html'

    def __unicode__(self):
        return "%s - welcome email" % self.user.username

    def get_email_headers(self):
        return {
            'From': 'Canubring <%s>' % self.from_email,
        }

    def get_recipients_list(self):
        return [self.user.email]

    def get_context(self):
        from django.core import signing
        from django.contrib.sites.models import Site
        domain = Site.objects.all()[0].domain
        salt = 'password_recovery'
        # url_salt = 'password_recovery_url'
        return {
            'token': signing.dumps(self.user.pk, salt=salt),
            'domain': domain,
        }


class CargoCommentNotification(Notification, NotificationMixin):
    obj = models.ForeignKey(CargoComment)

    from_email = settings.DEFAULT_FROM_EMAIL
    email_subject_tmpl = 'emails/cargo_comment_noti_subject.txt'
    email_plaintext_body_tmpl = 'emails/cargo_comment_noti_plaintext_body.txt'
    email_html_body_tmpl = 'emails/cargo_comment_noti_html_body.html'

    def __unicode__(self):
        return "%s - comment on cargo %s" % (self.user.username, self.obj.cargo.id)

    def get_email_headers(self):
        return {
            'From': 'Canubring <%s>' % self.from_email,
        }

    def get_recipients_list(self):
        return [self.user.email]

    def get_context(self):
        return {'sender': self.obj.user.get_full_name()}


class CargoFormNotification(Notification, NotificationMixin):
    obj = models.ForeignKey(Cargo)

    from_email = settings.DEFAULT_FROM_EMAIL
    email_subject_tmpl = 'emails/cargo_form_noti_subject.txt'
    email_plaintext_body_tmpl = 'emails/cargo_form_noti_plaintext_body.txt'
    email_html_body_tmpl = 'emails/cargo_form_noti_html_body.html'

    def __unicode__(self):
        return "%s - form on cargo %s" % (self.user.username, self.obj.id)

    def get_email_headers(self):
        return {
            'From': 'Canubring <%s>' % self.from_email,
        }

    def get_recipients_list(self):
        return [self.user.email]

    def get_context(self):
        return {'sender': self.obj.traveller_user.get_full_name()}


class CargoConfirmFormNotification(Notification, NotificationMixin):
    obj = models.ForeignKey(Cargo)

    from_email = settings.DEFAULT_FROM_EMAIL
    email_subject_tmpl = 'emails/cargo_confirm_form_noti_subject.txt'
    email_plaintext_body_tmpl = 'emails/cargo_confirm_form_noti_plaintext_body.txt'
    email_html_body_tmpl = 'emails/cargo_confirm_form_noti_html_body.html'

    def __unicode__(self):
        return "%s - confirm form on cargo %s" % (self.user.username, self.obj.id)

    def get_email_headers(self):
        return {
            'From': 'Canubring <%s>' % self.from_email,
        }

    def get_recipients_list(self):
        return [self.user.email]

    def get_context(self):
        return {'sender': self.obj.requesting_user.get_full_name()}


class CargoRejectFormNotification(Notification, NotificationMixin):
    obj = models.ForeignKey(Cargo)

    from_email = settings.DEFAULT_FROM_EMAIL
    email_subject_tmpl = 'emails/cargo_reject_form_noti_subject.txt'
    email_plaintext_body_tmpl = 'emails/cargo_reject_form_noti_plaintext_body.txt'
    email_html_body_tmpl = 'emails/cargo_reject_form_noti_html_body.html'

    def __unicode__(self):
        return "%s - reject form on cargo %s" % (self.user.username, self.obj.id)

    def get_email_headers(self):
        return {
            'From': 'Canubring <%s>' % self.from_email,
        }

    def get_recipients_list(self):
        return [self.user.email]

    def get_context(self):
        return {'sender': self.obj.requesting_user.get_full_name()}


class CargoDeliveryNotification(Notification, NotificationMixin):
    obj = models.ForeignKey(Cargo)

    from_email = settings.DEFAULT_FROM_EMAIL
    email_subject_tmpl = 'emails/cargo_delivery_form_noti_subject.txt'
    email_plaintext_body_tmpl = 'emails/cargo_delivery_form_noti_plaintext_body.txt'
    email_html_body_tmpl = 'emails/cargo_delivery_form_noti_html_body.html'

    def __unicode__(self):
        return "%s - delivery confirmed on cargo %s" % (self.user.username, self.obj.id)

    def get_email_headers(self):
        return {
            'From': 'Canubring <%s>' % self.from_email,
        }

    def get_recipients_list(self):
        return [self.user.email]

    def get_context(self):
        return {'sender': self.obj.requesting_user.get_full_name()}


class CargoReviewTravellerNotification(Notification, NotificationMixin):
    obj = models.ForeignKey(Cargo)

    from_email = settings.DEFAULT_FROM_EMAIL
    email_subject_tmpl = 'emails/cargo_review_traveller_form_noti_subject.txt'
    email_plaintext_body_tmpl = 'emails/cargo_review_traveller_form_noti_plaintext_body.txt'
    email_html_body_tmpl = 'emails/cargo_review_traveller_form_noti_html_body.html'

    def __unicode__(self):
        return "%s - traveller review on cargo %s" % (self.user.username, self.obj.id)

    def get_email_headers(self):
        return {
            'From': 'Canubring <%s>' % self.from_email,
        }

    def get_recipients_list(self):
        return [self.user.email]

    def get_context(self):
        return {'sender': self.obj.requesting_user.get_full_name()}


class CargoReviewReqUserNotification(Notification, NotificationMixin):
    obj = models.ForeignKey(Cargo)

    from_email = settings.DEFAULT_FROM_EMAIL
    email_subject_tmpl = 'emails/cargo_review_requesting_user_form_noti_subject.txt'
    email_plaintext_body_tmpl = 'emails/cargo_review_requesting_user_form_noti_plaintext_body.txt'
    email_html_body_tmpl = 'emails/cargo_review_requesting_user_form_noti_html_body.html'

    def __unicode__(self):
        return "%s - requesting user review on cargo %s" % (self.user.username, self.obj.id)

    def get_email_headers(self):
        return {
            'From': 'Canubring <%s>' % self.from_email,
        }

    def get_recipients_list(self):
        return [self.user.email]

    def get_context(self):
        return {'sender': self.obj.traveller_user.get_full_name()}


def send_email_notification(sender, instance, created, **kwargs):
    if created:
        instance.send_notification_email()

post_save.connect(send_email_notification, sender=CargoCommentNotification)
post_save.connect(send_email_notification, sender=CargoFormNotification)
post_save.connect(send_email_notification, sender=CargoConfirmFormNotification)
post_save.connect(send_email_notification, sender=CargoRejectFormNotification)
post_save.connect(send_email_notification, sender=CargoDeliveryNotification)
post_save.connect(send_email_notification, sender=CargoReviewTravellerNotification)
post_save.connect(send_email_notification, sender=CargoReviewReqUserNotification)
post_save.connect(send_email_notification, sender=WelcomeNotification)

