from datetime import datetime
from django.utils import timezone

from rest_framework import serializers

from notebook.models import Tag, Task, TaskTag


class TagSerializer(serializers.ModelSerializer):
    '''Serializer for tags.'''
    name = serializers.CharField()

    class Meta:
        model = Tag
        fields = ('name',)


class TaskSerializer(serializers.ModelSerializer):
    '''Serializer for tasks.'''
    tags = TagSerializer(required=False, many=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        if 'tags' not in self.initial_data:
            task = Task.objects.create(**validated_data)
            return task
        tags = validated_data.pop('tags')
        task = Task.objects.create(**validated_data)
        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(
                **tag
            )
            TaskTag.objects.create(tag=current_tag, task=task)
        return task

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.completed = validated_data.get(
            'completed', instance.completed
        )
        instance.completion_date = validated_data.get(
            'completion_date', instance.completion_date
        )

        if 'tags' not in validated_data:
            instance.save()
            return instance

        tags_data = validated_data.pop('tags')
        lst = []
        for tag in tags_data:
            current_tag, status = Tag.objects.get_or_create(
                **tag
            )
            lst.append(current_tag)
        instance.tags.set(lst)

        instance.save()
        return instance

    def validate(self, data):
        completed = self.initial_data.get('completed')
        completion_date = self.initial_data.get('completion_date')
        if datetime.strptime(
            completion_date, '%Y-%m-%dT%H:%M:%S.%fZ'
        ).replace(tzinfo=timezone.utc) < timezone.now() and not completed:
            raise serializers.ValidationError(
                'Установите корректную дату выполнения задания.'
            )
        return super().validate(data)
