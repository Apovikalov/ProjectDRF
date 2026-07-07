from django.urls.base import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from materials.models import Course, Lesson, CourseSubscription
from users.models import User

image_file = SimpleUploadedFile(
    name='C#.png',
    content=open('images/C#.png', 'rb').read(),
    content_type='image/png'
)


class MaterialTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        self.course = Course.objects.create(
            name='Programming on C#',
            description='Learn the C# language',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name='Lesson 1',
            description='Print in C#',
            course=self.course,
            owner=self.user
        )
        self.user.save()

    def test_create_lesson(self):
        """Тест создания урока"""
        data = {
            'name': 'Lesson 1',
            'description': 'Print in C#',
            'course': self.course.id,
            'owner': self.user.id
        }
        response = self.client.post(
            '/lessons/create/',
            data=data
        )

        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': 2, 'name': 'Lesson 1', 'description': 'Print in C#',
             'course': 1, 'image': None}
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):
        """Тестирование просмотра уроков"""

        response = self.client.get(
            '/lessons/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'id': 1, 'name': 'Lesson 1', 'description': 'Print in C#',
              'course': 1, 'image': None}]
        )

    def test_lesson_update(self):
        """Тестирование обновления уроков"""
        lesson_dict = {"name": "Python introduction"}

        response = self.client.patch('/lessons/update/1/', lesson_dict)

        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {'id': 1, 'name': 'Python introduction', 'description': 'Print in C#',
                          'course': 1, 'image': None})

    def test_lesson_delete(self):
        """Тестирование удаления уроков"""
        response = self.client.delete(
            '/lessons/delete/1/'
        )

        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionAPITestCase(APITestCase):
    """Тестирование функционала подписок на курсы."""

    def setUp(self):
        """Подготовка данных для тестов."""
        self.user = User.objects.create(email="test@mail.ru")
        self.course = Course.objects.create(name="python", owner=self.user)
        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        """Тестирование добавления подписки."""
        data = {"course_id": self.course.id}
        response = self.client.post('course/subscribe/', data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "подписка добавлена")
        self.assertTrue(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        """Тестирование удаления подписки (toggle)."""

        # Сначала создаем подписку
        CourseSubscription.objects.create(user=self.user, course=self.course)
        data = {"course_id": self.course.pk}
        response = self.client.post('course/subscribe/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "подписка удалена")
        self.assertFalse(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())
