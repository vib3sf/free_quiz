from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    can_revote = models.BooleanField()

    def get_absolute_url(self):
        return reverse('show_poll', kwargs={'poll_id': self.id})

    def user_completed_poll(self, user):
        return Vote.objects.filter(choice__question__poll=self, voter=user).exists()

    def user_can_vote(self, user):
        return self.can_revote or not self.user_completed_poll(user)

    @property
    def count_total_votes(self):
        return Vote.objects.filter(
            choice__question__poll=self, choice__question=Question.objects.filter(poll=self).first()).count()

    def __str__(self):
        return self.title


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    choice_text = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    @property
    def get_percent(self):
        count_votes = Vote.objects.filter(choice__question=self.question).count()
        return f'{self.vote_set.count() / count_votes * 100:.2f} %' if count_votes != 0 else ''

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.voter.username} - {self.choice.choice_text}'
