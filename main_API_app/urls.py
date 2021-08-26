from django.urls import path

from .views import (
    api_overview,
    login_user,
    logout_user,
    poll_create,
    poll_update,
    poll_delete,
    question_create,
    question_update,
    question_delete,
    all_active_polls,
    answer_create,
    all_answers_of_user,
)

urlpatterns = [
    path('', api_overview, name="api-overview"),

    path('login/', login_user, name="log-in"),
    path('logout/', logout_user, name="log-out"),

    path('poll/create/', poll_create, name="poll-create"),
    path('poll/update/<str:pk>/', poll_update, name="poll-update"),
    path('poll/delete/<str:pk>/', poll_delete, name="poll-delete"),

    path('question/create/', question_create, name="question-create"),
    path('question/update/<str:pk>/', question_update, name="question-update"),
    path('question/delete/<str:pk>/', question_delete, name="question-delete"),

    path('poll/all/', all_active_polls, name="all-polls"),

    path('answer/create/', answer_create, name="answer-create"),
    path('answer/all/user/', all_answers_of_user, name="all user's answers"),
]
