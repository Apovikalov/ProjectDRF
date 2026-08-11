from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_no_links


class LessonSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validate_no_links])

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'description', 'image', 'course')


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    name = serializers.CharField(validators=[validate_no_links])

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'
