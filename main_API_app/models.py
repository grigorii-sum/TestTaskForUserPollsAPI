from django.db import models
from django.conf import settings


class Poll(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    QUESTION_TYPES = (
        ('1', 'Ответ текстом'),
        ('2', 'Ответ с выбором одного варианта'),
        ('3', 'Ответ с выбором нескольких вариантов')
    )
    type = models.CharField(max_length=1, choices=QUESTION_TYPES)
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user_id) + " ANSWERED ON " + str(self.question_id) + ": '" + self.answer + "'"
