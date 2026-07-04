from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from materials.models import Course, Lesson
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
             'course': 1, 'image': None, 'owner': self.user.id}
        )

        self.assertTrue(
            Lesson.objects.all().exists()
        )


    def test_list_course(self):
        """Тест вывода списка курсов"""
        response = self.client.get(
            '/courses/'
        )

        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
