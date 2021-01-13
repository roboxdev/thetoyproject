from datetime import datetime
from unittest import mock

import factory
import pytz
from django.test import TestCase, Client

from .factories import ArticleFactory, WriterFactory, ApprovedArticleFactory, EditorFactory
from .models import Article, Writer


class TestDashboard(TestCase):
    def test_dashboard_writers(self):
        writer_1 = WriterFactory()
        writer_2 = WriterFactory()
        writer_3 = WriterFactory()

        with mock.patch('core.utils.timezone.now', return_value=datetime(2020, 3, 1, tzinfo=pytz.UTC)):
            factory.create_batch(
                Article,
                1,
                FACTORY_CLASS=ArticleFactory,
                written_by=writer_1,
            )
            factory.create_batch(
                Article,
                2,
                FACTORY_CLASS=ArticleFactory,
                written_by=writer_2,
            )
            factory.create_batch(
                Article,
                3,
                FACTORY_CLASS=ArticleFactory,
                written_by=writer_3,
            )

        with mock.patch('core.utils.timezone.now', return_value=datetime(2020, 3, 1, tzinfo=pytz.UTC)):
            factory.create_batch(
                Article,
                4,
                FACTORY_CLASS=ApprovedArticleFactory,
                written_by=writer_1,
            )
            factory.create_batch(
                Article,
                5,
                FACTORY_CLASS=ApprovedArticleFactory,
                written_by=writer_2,
            )
            factory.create_batch(
                Article,
                6,
                FACTORY_CLASS=ApprovedArticleFactory,
                written_by=writer_3,
            )

        with mock.patch('core.utils.timezone.now', return_value=datetime(2020, 1, 1, tzinfo=pytz.UTC)):
            factory.create_batch(
                Article,
                7,
                FACTORY_CLASS=ApprovedArticleFactory,
                written_by=writer_1,
            )
            factory.create_batch(
                Article,
                8,
                FACTORY_CLASS=ApprovedArticleFactory,
                written_by=writer_2,
            )
            factory.create_batch(
                Article,
                9,
                FACTORY_CLASS=ApprovedArticleFactory,
                written_by=writer_3,
            )
        with \
                mock.patch(
                    'core.utils.timezone.now',
                    return_value=datetime(2020, 3, 1, tzinfo=pytz.UTC),
                ), \
                self.assertNumQueries(1):
            writers = Writer.objects.with_articles_count()
            self.assertEqual(sum(w.total_articles for w in writers), 39)
            self.assertEqual(sum(w.total_articles_in_last_month for w in writers), 15)


class TestArticleApproval(TestCase):
    def setUp(self):
        self.editor = EditorFactory()
        factory.create_batch(
            Article,
            5,
            FACTORY_CLASS=ArticleFactory,
            status=Article.STATUS_APPROVED,
            edited_by=self.editor,
        )
        factory.create_batch(
            Article,
            10,
            FACTORY_CLASS=ArticleFactory,
        )

    def test_permissions(self):
        writer = WriterFactory()
        client = Client()
        client.force_login(writer.user)
        r = client.get('/article-approval')
        self.assertEqual(r.status_code, 403)

    def test_view(self):
        client = Client()
        client.force_login(self.editor.user)
        r = client.get('/article-approval')
        self.assertEqual(r.status_code, 200)
        object_list = r.context['object_list']
        self.assertEqual(len(object_list), 10)


class TestArticlesEdited(TestCase):
    def setUp(self):
        self.editor = EditorFactory()
        factory.create_batch(
            Article,
            5,
            FACTORY_CLASS=ArticleFactory,
            status=Article.STATUS_APPROVED,
            edited_by=self.editor,
        )
        factory.create_batch(
            Article,
            10,
            FACTORY_CLASS=ArticleFactory,
        )
        factory.create_batch(
            Article,
            15,
            FACTORY_CLASS=ArticleFactory,
            status=Article.STATUS_APPROVED,
            edited_by=EditorFactory(),
        )

    def test_permissions(self):
        writer = WriterFactory()
        client = Client()
        client.force_login(writer.user)
        r = client.get('/articles-edited')
        self.assertEqual(r.status_code, 403)

    def test_view(self):
        client = Client()
        client.force_login(self.editor.user)
        r = client.get('/articles-edited')
        self.assertEqual(r.status_code, 200)
        object_list = r.context['object_list']
        self.assertEqual(len(object_list), 5)
