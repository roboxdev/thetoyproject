from django.urls import path

from .views import (
    DashboardView,
    ArticleCreateView,
    ArticleDetailView,
    ArticleApprovalView,
    ArticlesEditedView,
    ArticleApprovalPostView,
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard-view'),
    path('article/<pk>', ArticleDetailView.as_view(), name='article-detail-view'),
    path('article', ArticleCreateView.as_view(), name='article-detail-view'),
    path('article-approval/<pk>', ArticleApprovalPostView.as_view(), name='article-approval-view'),
    path('article-approval', ArticleApprovalView.as_view(), name='article-approval-view'),
    path('articles-edited', ArticlesEditedView.as_view(), name='articles-edited-view'),
]
