from django.db import models
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from users.models import CustomUser
from management.models import (PublicFile, ProtectedImage, ProtectedFile)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from smtplib import SMTPException
from sportassociation import settings


class Weekmail(models.Model):
    """Model representing a mail meant to be sent weekly.

    Attributes:
        - conclusion: string storing the conclusion paragraph of the weekmail.
        - creation_date: datetime of the creation of the weekmail. Not editable.
        - introduction: string storing the introduction paragraph of the weekmail.
        - modification_date: datetime of the last modification of the weekmail.
            Not editable.
        - sent_date: datetime of the date when the weekmail was sent. Can be
            None ("draft" mode).
        - subject: string storing the title of the weekmail which is also the
            subject of the mail.

    Relationships with other models:
        - attached: several files destined to the public which will be attached
            to the weekmail.
        - paragraphs: several paragraphs associated to this weekmail.

    Ordering by DESCending sent_date
    """

    conclusion = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    introduction = models.TextField()
    modification_date = models.DateTimeField(auto_now=True)
    sent_date = models.DateTimeField(default=None, null=True, blank=True,
                db_index=True)
    subject = models.CharField(max_length=80, db_index=True)

    attached = GenericRelation(PublicFile, related_query_name='weekmails',
                blank=True)

    class Meta:
        verbose_name = _('weekmail')
        verbose_name_plural = _('weekmails')
        ordering = ['-sent_date']

    def __str__(self):
        return '%s' % (self.subject)

    def send(self):
        #Create the weekmail content and send it.
        content = {'weekmail': self}
        mail_content_txt = render_to_string('communication/weekmail.txt',
                                            content)
        mail_content_html = render_to_string('communication/weekmail.html',
                                            content)

        #You can change the weekmail recipients here.
        recipients = settings.WEEKMAIL_RECIPIENTS
        sender = settings.DEFAULT_FROM_EMAIL
        try:
            mail = EmailMultiAlternatives()
            mail.subject = _('[Weekmail] %s') % (self.subject)
            mail.body = mail_content_txt
            mail.from_email = sender
            mail.to = recipients
            mail.cc = [sender,]
            mail.attach_alternative(mail_content_html, "text/html")
            for attachment in self.attached.all():
                print(attachment.file.path)
                mail.attach_file(attachment.file.path)
            mail.send()
            self.sent_date = timezone.now()
            self.save()
            return True
        except SMTPException:
            return False
        return False


class Paragraph(models.Model):
    """Paragraph of a weekmail.

    Attributes:
        - content: string storing the content of the paragraph.
        - creation_date: datetime of the creation of the paragraph. Not editable.
        - modification_date: datetime of the last modification of the paragraph.
            Not editable.
        - index: integer indicating the index of the paragraph among all
            paragraphs in the weekmail.
        - title: string storing the title of the paragraph.

    Relationships with other models:
        - weekmail: weekmail associated to this paragraph.

    Ordering by ASCending index
    """

    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    index = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=50)

    weekmail = models.ForeignKey(Weekmail, related_name='paragraphs')

    class Meta:
        verbose_name = _('paragraph')
        verbose_name_plural = _('paragraphs')
        ordering = ['index']

    def __str__(self):
        return '%s (%s)' % (self.title, self.weekmail.subject)

    # TODO: Guarantee uniqueness of index in a weekmail
    # Comment (@qschulz): using InlineSortable in Admin does the trick with JS


class Article(models.Model):
    """Model representing an article.

    Attributes:
        - content: string storing the content of the article.
        - cover: image illustrating the article. Can be None.
        - creation_date: datetime of the creation of the article. Not editable.
        - is_frontpage: boolean indicating if the article should be displayed on
            the front-page.
        - modification_date: datetime of the last modification of the article.
            Not editable.
        - publication_date: datetime of the publication of the article. Can be
            "in the future". Can be None ("draft" mode).
        - slug: string only used for SEO.
        - summary: string storing the summary of the article used when displaying
            articles in compact mode. Can be None.
        - title: string storing the title of the article.

    Relationships with other models:
        - attached_files: several files destined to registered users.
        - attached_photos: several files destined to registered users.
        - author: author of the article.
        - matches: several matches associated to this article. Typically, the
            article will give report on these matches.

    Ordering by DESCending publication_date.
    """

    content = models.TextField()
    cover = ImageField(upload_to='public/covers/articles/', null=True,
            blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_frontpage = models.BooleanField(default=False, db_index=True)
    modification_date = models.DateTimeField(auto_now=True)
    publication_date = models.DateTimeField(db_index=True, null=True, blank=True)
    slug = models.SlugField()
    summary = models.CharField(max_length=180, null=True, blank=True)
    title = models.CharField(max_length=50, db_index=True)

    attached_files = GenericRelation(ProtectedFile, blank=True)
    attached_photos = GenericRelation(ProtectedImage, blank=True)
    author = models.ForeignKey(CustomUser, related_name='authored_articles',
                null=True, blank=True, on_delete=models.SET_NULL, default=None)

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ['-publication_date']

    def __str__(self):
        return '%s' % (self.title)


class Information(models.Model):
    """Model representing an information.

    The information is most likely to be displayed on the front page to give short
    and important information. It is separated from article because information
    will be displayed only for a certain amount of time and not available for
    users in archives.

    Attributes:
        - content: string storing the content of the information. Can be None.
        - end_date: datetime of the end of the publication of the information.
        - is_important: boolean to set the color of the message on the frontpage.
        - is_published: boolean indicating if the information is published yet.
        - start_date: datetime of the start of the publication of the article.
            Can be "in the future". Can be None ("draft" mode).
        - title: string storing the title of the information. Can be None.

    Ordering by ASCending start_date then DESCending end_date.

    Clean:
        - start_date cannot be after end_date.
        - at least the title or the content has to be set.
    """

    content = models.TextField(blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_important = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False, db_index=True)
    start_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = _('information')
        verbose_name_plural = _('informations')
        ordering = ['start_date', '-end_date']

    def clean(self):
        if self.start_date is not None and self.end_date is not None and\
                self.start_date >= self.end_date:
            raise ValidationError(_('Start date cannot be after end date.'))
        if not self.title and not self.content:
            raise ValidationError(_('At least title or content should be set.'))

    def __str__(self):
        return '%s' % (self.title)
