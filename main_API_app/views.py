from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView

from .models import Poll, Question, Answer
from .serializers import UserSerializer, PollSerializer, QuestionSerializer, AnswerSerializer


@api_view(['POST'])
def login_user(request):
    username = request.data["username"]
    password = request.data["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        user_profile = User.objects.get(username=username)
        serializer = UserSerializer(user_profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def logout_user(request):
    logout(request)

    return Response(status=status.HTTP_200_OK)


class CreatePollAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class UpdatePollAPIView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def perform_update(self, serializer):
        poll = Poll.objects.get(pk=self.queryset.values('id').last()["id"])
        start_date = serializer.validated_data["start_date"]
        end_date = serializer.validated_data["end_date"]

        if poll.start_date == start_date and start_date < end_date:
            serializer.save()


class DeletePollAPIView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class CreateQuestionAPIView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class UpdateQuestionAPIView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class DeleteQuestionAPIView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ListActivePollsAPIView(ListAPIView):
    queryset = Poll.objects.filter(is_active=True)
    serializer_class = PollSerializer


class CreateAnswerAPIView(CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ListUsersAnswersAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(user_id=self.request.user)
