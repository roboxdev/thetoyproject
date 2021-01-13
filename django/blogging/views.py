from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, ListView

from .models import Writer, Article


class DashboardView(ListView):
    template_name = 'blogging/dashboard.html'
    model = Writer
    queryset = Writer.objects.with_articles_count()


class ArticleDetailView(DetailView):
    template_name = 'blogging/article_detail.html'


class ArticleApprovalView(PermissionRequiredMixin, ListView):
    permission_required = 'blogging.can_approve_articles'
    template_name = 'blogging/article_approval.html'

    def get_queryset(self):
        return Article.objects.approval_needed()


class ArticlesEditedView(PermissionRequiredMixin, ListView):
    permission_required = 'blogging.can_approve_articles'
    template_name = 'blogging/articles_edited.html'

    def get_queryset(self):
        user = self.request.user
        return Article.objects.edited_by_user(user)
