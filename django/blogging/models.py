from datetime import timedelta

from django.conf import settings
from django.db import models

from django.db.models import Count, Q

from core.utils import get_current_time


class WriterManager(models.Manager):
    def with_articles_count(self):
        return self.annotate(
            total_articles=Count(
                'articles',
                filter=Q(
                    articles__status=Article.STATUS_APPROVED,
                )
            ),
            total_articles_in_last_month=Count(
                'articles',
                filter=Q(
                    articles__status=Article.STATUS_APPROVED,
                    articles__created_at__gte=get_current_time() - timedelta(days=30),
                )
            ),
        )


class Writer(models.Model):
    class Meta:
        permissions = [
            ("can_approve_articles", "Can change the status of articles"),
        ]
    objects = WriterManager()

    is_editor = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='writer',
    )

    def __str__(self):
        return self.name


class ArticleManager(models.Manager):
    def edited_by_user(self, user):
        return self.filter(
            Q(edited_by__user=user),
            Q(status=Article.STATUS_APPROVED) | Q(status=Article.STATUS_REJECTED)
        )

    def approval_needed(self):
        return self.filter(status=Article.STATUS_PENDING)


class Article(models.Model):
    objects = ArticleManager()

    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = (
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_APPROVED, STATUS_APPROVED),
        (STATUS_REJECTED, STATUS_REJECTED),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    written_by = models.ForeignKey(
        Writer,
        on_delete=models.CASCADE,
        related_name='articles',
    )
    edited_by = models.ForeignKey(
        Writer,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='edited_articles',
    )

    def __str__(self):
        return self.title

    def approve(self, writer):
        if self.status == self.STATUS_PENDING:
            self.status = self.STATUS_APPROVED
            self.edited_by = writer
            self.save()

    def reject(self, writer):
        if self.status == self.STATUS_PENDING:
            self.status = self.STATUS_REJECTED
            self.edited_by = writer
            self.save()
