from django.urls import path
from .views import RegisterView, LoginView, FileUploadView, GenerateSummaryView, HistoryView, DeleteSummaryView, AskQuestionView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload/', FileUploadView.as_view(), name='upload'),
    path('generate-summary/', GenerateSummaryView.as_view(), name='generate-summary'),
    path('history/', HistoryView.as_view(), name='history'),
    path('delete-summary/<int:summary_id>/', DeleteSummaryView.as_view(), name='delete-summary'),
    path("ask-question/", AskQuestionView.as_view(), name="ask-question"),
]