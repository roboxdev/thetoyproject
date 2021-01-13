from datetime import timedelta

import factory
from django.contrib.auth.models import Permission

from core.factories import UserFactory
from core.utils import get_current_time
from . import models


class WriterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Writer
    name = factory.Faker('name')
    user = factory.SubFactory(UserFactory)
    is_editor = False


class EditorFactory(WriterFactory):
    is_editor = True

    @factory.post_generation
    def add_permissions(self, create, extracted, **kwargs):
        permission = Permission.objects.get(codename='can_approve_articles')
        self.user.user_permissions.add(permission)


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Article
    created_at = get_current_time() - timedelta(days=100)
    title = factory.Faker('name')
    content = factory.Faker('text')
    status = models.Article.STATUS_PENDING
    written_by = factory.SubFactory(WriterFactory)
    edited_by = None


class ApprovedArticleFactory(ArticleFactory):
    status = models.Article.STATUS_APPROVED


class RejectedArticleFactory(ArticleFactory):
    status = models.Article.STATUS_REJECTED


class EditedArticleFactory(ArticleFactory):
    edited_by = factory.SubFactory(EditorFactory)
