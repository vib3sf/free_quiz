from rest_framework import serializers

from polls.models import Poll, Question, Choice, Vote


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text', )

    def to_representation(self, instance):
        json = super().to_representation(instance)
        json['percent'] = instance.get_percent
        return json


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, write_only=True)

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'choices')

    def to_representation(self, instance):
        json = super().to_representation(instance)
        json['choices'] = ChoiceSerializer(instance.choice_set.all(), many=True).data
        return json


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, write_only=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Poll
        fields = '__all__'

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        poll = Poll.objects.create(**validated_data)
        for question_data in questions_data:
            choices_data = question_data.pop('choices')
            question = Question.objects.create(poll=poll, **question_data)
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)
        return poll

    def to_representation(self, instance):
        json = super().to_representation(instance)
        json['questions'] = QuestionSerializer(instance.question_set.all(), many=True).data
        json['total_votes'] = instance.count_total_votes
        return json


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('choice', )


class VoteListSerializer(serializers.ListSerializer):
    child = VoteSerializer()
