from django.urls import path

from .views import (
    login_user,
    logout_user,
    CreatePollAPIView,
    UpdatePollAPIView,
    DeletePollAPIView,
    CreateQuestionAPIView,
    UpdateQuestionAPIView,
    DeleteQuestionAPIView,
    ListActivePollsAPIView,
    CreateAnswerAPIView,
    ListUsersAnswersAPIView
)

urlpatterns = [
    path('login/', login_user, name="log-in"),
    path('logout/', logout_user, name="log-out"),

    path('poll/create/', CreatePollAPIView.as_view(), name="poll-create"),
    path('poll/update/<str:pk>/', UpdatePollAPIView.as_view(), name="poll-update"),
    path('poll/delete/<str:pk>/', DeletePollAPIView.as_view(), name="poll-delete"),

    path('question/create/', CreateQuestionAPIView.as_view(), name="question-create"),
    path('question/update/<str:pk>/', UpdateQuestionAPIView.as_view(), name="question-update"),
    path('question/delete/<str:pk>/', DeleteQuestionAPIView.as_view(), name="question-delete"),

    path('poll/all/', ListActivePollsAPIView.as_view(), name="all-polls"),

    path('answer/create/', CreateAnswerAPIView.as_view(), name="answer-create"),
    path('answer/all/user/', ListUsersAnswersAPIView.as_view(), name="all user's answers"),
]
