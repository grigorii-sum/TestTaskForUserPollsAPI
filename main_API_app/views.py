from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Poll, Question, Answer
from .serializers import UserSerializer, PollSerializer, QuestionSerializer, AnswerSerializer


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Log in': 'login/',
        'Log out': 'logout/',

        'Poll create': 'poll/create/',
        'Poll update': 'poll/update/<str:pk>/',
        'Poll delete': 'poll/delete/<str:pk>/',

        'Question create': 'question/create/',
        'Question update': 'question/update/<str:pk>/',
        'Question delete': 'question/delete/<str:pk>/',

        'All polls': 'poll/all/',
        'Answer create': 'answer/create/',
        'All answers of user': 'answer/all/user/'
    }

    return Response(api_urls, status=status.HTTP_200_OK)


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


@login_required
@api_view(['POST'])
def poll_create(request):
    if request.user.is_superuser:
        serializer = PollSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_403_FORBIDDEN)


@login_required
@api_view(['PATCH'])
def poll_update(request, pk):
    if request.user.is_superuser:
        required_poll = Poll.objects.get(id=pk)

        if request.data["start_date"] != required_poll.start_date:
            return Response("Start_date cannot be changed", status=status.HTTP_400_BAD_REQUEST)

        serializer = PollSerializer(instance=required_poll, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_403_FORBIDDEN)


@login_required
@api_view(['DELETE'])
def poll_delete(request, pk):
    if request.user.is_superuser:
        required_poll = Poll.objects.get(id=pk)
        required_poll.delete()

        return Response('Poll successfully deleted', status=status.HTTP_200_OK)

    return Response(status=status.HTTP_403_FORBIDDEN)


@login_required
@api_view(['POST'])
def question_create(request):
    if request.user.is_superuser:
        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_403_FORBIDDEN)


@login_required
@api_view(['PATCH'])
def question_update(request, pk):
    if request.user.is_superuser:
        required_question = Question.objects.get(id=pk)
        serializer = QuestionSerializer(instance=required_question, data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_403_FORBIDDEN)


@login_required
@api_view(['DELETE'])
def question_delete(request, pk):
    if request.user.is_superuser:
        required_question = Question.objects.get(id=pk)
        required_question.delete()

        return Response('Question successfully deleted', status=status.HTTP_200_OK)

    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def all_active_polls(request):
    all_polls = Poll.objects.all()
    serializer = PollSerializer(all_polls, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def answer_create(request):
    serializer = AnswerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@login_required
@api_view(['GET'])
def all_answers_of_user(request):
    all_required_answers = Answer.objects.filter(user_id=request.user)
    serializer = AnswerSerializer(all_required_answers, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
