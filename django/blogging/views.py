from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from .models import Writer, Article


class DashboardView(ListView):
    template_name = 'blogging/dashboard.html'
    model = Writer
    queryset = Writer.objects.with_articles_count()


class ArticleDetailView(DetailView):
    template_name = 'blogging/article_detail.html'
    model = Article


class ArticleCreateView(CreateView):
    template_name = 'blogging/article_detail.html'
    template_name_suffix = ''
    model = Article
    fields = ('title', 'content')

    def form_valid(self, form):
        form.instance.written_by = self.request.user.writer
        return super(ArticleCreateView, self).form_valid(form)


class ArticleApprovalView(PermissionRequiredMixin, ListView):
    permission_required = 'blogging.can_approve_articles'
    template_name = 'blogging/article_approval.html'
    queryset = Article.objects.approval_needed()


class ArticleApprovalPostView(PermissionRequiredMixin, UpdateView):

    permission_required = 'blogging.can_approve_articles'
    model = Article
    fields = ['status']
    template_name = 'blogging/articles_edited.html'

    def form_valid(self, form):
        form.instance.edited_by = self.request.user.writer
        return super(ArticleApprovalPostView, self).form_valid(form)

    def get_success_url(self):
        # To stay on the same page
        return self.request.META.get('HTTP_REFERER', '/')


class ArticlesEditedView(PermissionRequiredMixin, ListView):
    permission_required = 'blogging.can_approve_articles'
    template_name = 'blogging/articles_edited.html'

    def get_queryset(self):
        user = self.request.user
        return Article.objects.edited_by_user(user)
