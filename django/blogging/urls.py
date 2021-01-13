from django.urls import path

from .views import DashboardView, ArticleDetailView, ArticleApprovalView, ArticlesEditedView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard-view'),
    path('article/<article_id>', ArticleDetailView.as_view(), name='article-detail-view'),
    path('article-approval', ArticleApprovalView.as_view(), name='article-approval-view'),
    path('articles-edited', ArticlesEditedView.as_view(), name='articles-edited-view'),
]
