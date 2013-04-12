from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from notifier.models import Notification, NotificationMixin
from cargos.models import CargoComment


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

def send_email_notification(sender, instance, created, **kwargs):
    if created:
        instance.send_notification_email()

post_save.connect(send_email_notification, sender=CargoCommentNotification)

